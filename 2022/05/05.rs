#![feature(iter_array_chunks)]
use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;
use std::vec::Vec;

fn main() {
    let mut lines = read_lines("./05/05.txt").unwrap().map(|l| l.unwrap());
    let mut stacks: Vec<String> = vec![];

    for line in &mut lines {
        if line.len() == 0 {
            break;
        }
        line[1..]
            .chars()
            .step_by(4)
            .enumerate()
            .for_each(|(i, chunk)| {
                if stacks.len() < i + 1 {
                    stacks.push(String::new());
                }
                // println!("{} {}", &i, &chunk);
                if chunk != ' ' {
                    stacks[i].insert(0, chunk);
                }
            });
    }

    for line in &mut lines {
        let moves: Vec<&str> = line.split(" ").collect();

        // println!("{} {} {}", count, from, to);

        if let [count, from, to] = moves[1..]
            .iter()
            .step_by(2)
            .map(|n| n.parse::<usize>().unwrap())
            .collect::<Vec<usize>>()[..]
        {
            for _ in 0..count {
                let item = stacks[from - 1].pop().unwrap();
                stacks[to - 1].push(item);
            }
        } else {
            println!("Bad move!")
        }
    }

    println!(
        "{}",
        stacks
            .iter_mut()
            .map(|s| s.chars().rev().next().unwrap())
            .collect::<String>()
    );

    // for i in 0..stacks.len() {
    //     print!("{}", stacks[i].pop().unwrap());
    // }

    println!();
}

fn read_lines<P>(filename: P) -> io::Result<io::Lines<io::BufReader<File>>>
where
    P: AsRef<Path>,
{
    let file = File::open(filename)?;
    Ok(io::BufReader::new(file).lines())
}
