use crate::dice::DiceCache;
use regex::Regex;
use lazy_static::lazy_static;

// `lazy_static!` macro generates static instances for regex patterns
// to avoid repeated runtime compilation of these patterns.
lazy_static! {
    static ref SIGN_RX : Regex = Regex::new(r"^ *(?<sign>[-+]) *").unwrap();
    static ref DICE_ROLL_RX : Regex = Regex::new(r"^(?<count>\d+)[dD](?<faces>\d+) *(?<descriptor>\([^)]*\))?").unwrap();
    static ref ALGEBRIC_ELEMENT_RX : Regex = Regex::new(r"^(?<amount>\d+) *(?<descriptor>\([^)]*\))?").unwrap();
}

// Represents a roll of a dice with specified number of faces and count.
#[derive(Debug)]
#[allow(dead_code)]
pub struct DiceRoll {
  pub count: u32,
  pub faces: u32,
  pub descriptor: Option<String>,
  pub positive: bool,
}

// Represents an algebraic element which involves an amount 
// that could be positive or negative (controlled by the `positive` field).
#[derive(Debug)]
#[allow(dead_code)]
pub struct AlgebraicElement {
  pub amount: u32,
  pub positive: bool,
  pub descriptor: Option<String>,
}

// Enum that can either represent a dice roll or an algebraic element.
#[derive(Debug)]
pub enum RollPart {
  DiceRoll(DiceRoll),
  AlgebraicElement(AlgebraicElement),
}

impl RollPart {
  pub fn positive(&self) -> bool {
    match self {
      RollPart::DiceRoll(dr) => dr.positive,
      RollPart::AlgebraicElement(a) => a.positive,
    }
  }

  pub fn descriptor(&self) -> Option<&str> {
    match self {
      RollPart::DiceRoll(dr) => dr.descriptor.as_deref(),
      RollPart::AlgebraicElement(a) => a.descriptor.as_deref(),
    }
  }

  pub fn as_string(&self) -> String {
    match self {
      RollPart::DiceRoll(dr) => {
        let mut s = String::new();
        s.push_str(if dr.positive { "+" } else { "-" });
        s.push_str(&format!("{}d{}", dr.count, dr.faces));
        if let Some(ref d) = dr.descriptor {
          s.push_str(&format!(" {}", d));
        };
        s
      }
    
      RollPart::AlgebraicElement(a) => {
        let mut s = String::new();
        s.push_str(if a.positive {"+"} else {"-"});
        s.push_str(&format!("{}", a.amount));
        if let Some(ref d) = a.descriptor {
          s.push_str(&format!(" {}", d));
        };
        s
      }
    }
  }
}

pub type RollParts = Vec<RollPart>;

pub fn string_to_parts(string: &str) -> Result<RollParts, &'static str> {
  let mut ret = Vec::new();
  let mut start: usize = 0;
  let string_len = string.len();
  let mut positive = true;

  loop {
    let mut slice = &string[start..string_len];

    if start == 0 {
      if let Some(caps) = SIGN_RX.captures(slice) {
        positive = &caps["sign"] == "+";
        start += caps[0].len();
      }
    } else if let Some(caps) = SIGN_RX.captures(slice) {
      positive = &caps["sign"] == "+";
      start += caps[0].len();
    } else {
      return Err("Wrong formatting in the dice roll string: Missing sign");
    }

    slice = &string[start..string_len];

    if let Some(caps) = DICE_ROLL_RX.captures(slice) {
      let count: u32 = caps["count"].parse().unwrap();
      let faces: u32 = caps["faces"].parse().unwrap();
      ret.push(
        RollPart::DiceRoll(
          DiceRoll {
            positive,
            count,
            faces,
            descriptor: caps.name("descriptor").map(|s| String::from(s.as_str())),
          }
        )
      );

      start += caps[0].len();
    } else if let Some(caps) = ALGEBRIC_ELEMENT_RX.captures(slice) {
      let amount: u32 = caps["amount"].parse().unwrap();

      ret.push(RollPart::AlgebraicElement(AlgebraicElement {
        positive,
        amount,
        descriptor: caps.name("descriptor").map(|s| String::from(s.as_str())),
      }));

      start += caps[0].len();
    } else {
      return Err("Wrong formatting in the dice roll string: Unidentified RollPart");
    }

    if start == string_len { break; }
  }

  Ok(ret)
}

#[derive(Debug)]
#[allow(dead_code)]
pub struct PartResult {
  pub part: RollPart,
  pub results: Vec<u32>,
  pub total: u32,
}

impl PartResult {
  pub fn descriptor(&self) -> Option<&str> {
    self.part.descriptor()
  }

  pub fn total_i64(&self) -> i64 {
    if self.part.positive() { 
      self.total as i64 
    } else {
      0i64 - self.total as i64
    }
  }
}

pub type PartResults = Vec<PartResult>;

// Struct representing a dice roller, which internally uses a cache of dices.
pub struct DiceRoller {
  pub dices: DiceCache,
}

impl DiceRoller {
  // Constructs a new DiceRoller with an internal cache of dices.
  pub fn new() -> Self {
    Self { dices: DiceCache::new() }
  }

  pub fn parts_to_result(&mut self, parts: RollParts) -> i64 {
    let mut ret : i64 = 0;
    for part in parts {
      match &part {
        RollPart::AlgebraicElement(a) => ret += a.amount as i64 * (if part.positive() {1} else {-1}),
        RollPart::DiceRoll(dr) => {
          let dice = self.dices.get(dr.faces);
          for _ in 0..dr.count {
            ret += dice.roll() as i64 * (if part.positive() {1} else {-1});
          }
        }
      }
    }
    ret
  }

  pub fn parts_to_results(&mut self, parts: RollParts) -> PartResults {
    let mut ret = PartResults::new();
    for part in parts {
      let mut results: Vec<u32> = Vec::new();
      match &part {
        RollPart::AlgebraicElement(a) => results.push(a.amount),
        RollPart::DiceRoll(dr) => {
          let dice = self.dices.get(dr.faces);
          for _ in 0..dr.count {
            results.push(dice.roll());
          }
        }
      }
      ret.push(
        PartResult {
          total: results.iter().sum(),
          part,
          results,
        }
      )
    }
    ret
  }

  pub fn string_to_results(&mut self, string : &str) -> Result<PartResults, &'static str> {
    string_to_parts(string).map(|parts| self.parts_to_results(parts))
  }
  pub fn string_to_result(&mut self, string: &str) -> Result<i64, &'static str> {
    string_to_parts(string).map(|parts| self.parts_to_result(parts))
  }
}
