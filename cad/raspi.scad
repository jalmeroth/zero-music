include<standoff.scad>;

module raspi(){
    $h=5;
    $d1=5.2;
    $d2=2.8;

    //translate([64,29,0])
    translate([6.2,29.4,0])
    color("green")
    standoff($h,$d1,$d2);

    //translate([-29,11.5,0])
    translate([64.2,29.4,0])
    color("blue")
    standoff($h,$d1,$d2);

    translate([6.2,6.3,0])
    color("pink")
    standoff($h,$d1,$d2);

    translate([64.2,6.3,0])
    color("red")
    standoff($h,$d1,$d2);
}