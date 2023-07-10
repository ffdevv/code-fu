use rand::Rng;
use rand::distributions::uniform::SampleUniform;

pub fn from_to<T: SampleUniform + PartialOrd>
(from: T, to: T) -> T
{
  let mut rng = rand::thread_rng();
  rng.gen_range(from..=to)
}

pub fn choice<T>
(data: &[T]) -> &T
{
  let mut rng = rand::thread_rng();
  let index : usize = rng.gen_range(0..data.len());
  &data[index]
}
