use rustroller::DiceRoller;
use clap::Parser;

#[derive(Parser, Debug)]
#[command(name = "RustRoller")]
#[command(author = "ffdevv")]
#[command(version = "1.0")]
#[command(about = "D&D ftw", long_about = None)]
struct Args {
  // string of dices that must be rolled
  dices_string: Option<String>,

  // times the roll has to be repeated
  #[arg(short, long, default_value_t = 1)]
  repeat: u16,

  // verbose
  #[arg(short, long, action = clap::ArgAction::Count)]
  verbose: u8,
}

fn mean(totals: &Vec<i64>) -> Option<f64> {
  if totals.is_empty() {
    None
  } else {
    Some(totals.iter().sum::<i64>() as f64 / totals.len() as f64)
  }
}

fn main() {
  let args = Args::parse();
  let mut roller = DiceRoller::new();

  let dices_string = match args.dices_string.as_deref() {
    Some(s) => s,
    None => "1d20"
  };

  let mut totals: Vec<i64> = Vec::new();

  match args.verbose {

    0 => {
      for _ in 0..args.repeat {
        let result = roller
          .string_to_result(dices_string)
          .unwrap_or_else(|e| panic!("{}", e));
        println!("{}", result);
        totals.push(result);
      }
    },

    1 =>  {
      for _ in 0..args.repeat {
        let results = roller
          .string_to_results(dices_string)
          .unwrap_or_else(|e| panic!("{}", e));  
        let mut subtotal : i64 = 0;
        for part_result in results.iter() {
          println!("{}: {}", part_result.part.as_string(), part_result.total);
          subtotal += part_result.total_i64();
        }
        totals.push(subtotal);
        println!("___ {}", subtotal);
      }
    },

    2 =>  {
      for _ in 0..args.repeat {
        let results = roller
          .string_to_results(dices_string)
          .unwrap_or_else(|e| panic!("{}", e));  
        let mut subtotal : i64 = 0;
        for part_result in results.iter() {
          subtotal += part_result.total_i64();
          println!("{}: {}", 
            part_result.part.as_string(), 
            part_result.total,
          );
          for (i, dice_result) in part_result.results.iter().enumerate() {
            println!("    dice {}: {}", i+1, dice_result);
          }
        }
        totals.push(subtotal);
        println!("___ {}", subtotal);
      }
    },

    _ =>  {
      for _ in 0..args.repeat {
        let results = roller
          .string_to_results(dices_string)
          .unwrap_or_else(|e| panic!("{}", e));  
        let mut subtotal : i64 = 0;
        for part_result in results.iter() {
          subtotal += part_result.total_i64();
          println!("{:?}", part_result);
        }
        totals.push(subtotal);
        println!("___ {}", subtotal);
      }
    },
  }

  if args.repeat > 1 {
    println!("----");
    println!("mean: {}", mean(&totals).unwrap());
  }

}
