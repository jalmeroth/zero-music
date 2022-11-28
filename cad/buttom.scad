include<raspi.scad>;
$fn=100;

module buttom($x, $y, $ws) {
    $ds=1.5;        //boden stärke
    $bx=$x-2*$ws;   //box breite
    $by=$y-2*$ws;   //box tiefe
    $bz=20;         //box höhe

    $ax=12;
    $az=8;

    difference() {
        color("blue")
        cube([$bx, $by, $bz]);
        translate([$ws, $ws, $ds])
        color("red")
        cube([$bx-2*$ws, $by-2*$ws, $bz-$ds]);
        translate([($bx-$ax)/2, 0, $ds])
        cube([$ax, $ws, $az]);
    }
    rotate([90,0,90])
    translate([$by/2,$bz/2,-$ws])
    cylinder(h=2*$ws,d=3);
    rotate([90,0,90])
    translate([$by/2,$bz/2,$bx-$ws])
    cylinder(h=2*$ws,d=3);
}
$ws=2.4;
$ds=1.5;

buttom(150, 100, $ws);

translate([20,30,$ds])
raspi();
