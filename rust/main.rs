fn study_var() {
    let x: i32 = 8;
    {
        println!("{}", x);
        let x = 12;
        println!("{}", x);
    }
    println!("{}", x);
    let x = 42;
    println!("{}", x);
}

fn study_varshadowing() {
    let mut v = Vec::new();
    v.push(1);
    v.push(2);
    v.push(3);
    let v = v;
    for i in &v {
        println!("{}", i);
    }
}

fn study_type() {
    let elem = 5u8;
    let mut vec = Vec::new();
    vec.push(elem);
    // println!("{:?}", vec);

    let p = (1i32, 2i32);
    let (a, b) = p;
    println!("{} {}", a, b);
}

fn main() {
    // study_var();
    // study_varshadowing();
    study_type();
}
