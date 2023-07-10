use crate::random;
use std::collections::HashMap;

pub struct Dice {
  pub faces: u32,
}

impl Dice {
  pub fn roll
  (&self) -> u32 
  {
    random::from_to(1, self.faces)
  }
}

pub struct DiceCache {
  dice: HashMap<u32, Dice>,
}

impl DiceCache {
  pub fn new() -> Self {
    Self {
      dice: HashMap::new(),
    }
  }

  pub fn get(&mut self, faces: u32) -> &Dice {
    if !self.dice.contains_key(&faces) {
      self.dice.insert(faces, Dice { faces });
    }
    self.dice.get(&faces).expect("Cache should never miss")
  }
}
