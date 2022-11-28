include<rfid.scad>;

$fn=100;
$ds=1.5;        //boden stärke
$ws=2.4;        //wand stärke
$bx=150;        //box breite
$by=100;        //box tiefe
$bz=40;         //box höhe

$d1=24;         //durchmesser knopf
$r1=$d1/2;      //radius knopf

$d2=8;          //durchmesser LED
$r2=$d2/2;      //radius LED
$s1=2*$ws;      //space für knöpfe

difference() {
    // Box
    cube([$bx,$by,$bz]);
    translate([$ws,$ws,$ds])
    cube([$bx-2*$ws,$by-2*$ws,$bz-$ds]);
    
    // Knöpfe
    translate([$r1 + $s1, $r1 + $s1, 0])
    cylinder(h=$ds, d=$d1);
    
    translate([$bx - $r1 - $s1, $r1 + $s1, 0])
    cylinder(h=$ds, d=$d1);

    translate([$r1 + $s1, $by - $r1 - $s1, 0])
    cylinder(h=$ds, d=$d1);

    translate([$bx - $r1 - $s1, $by - $r1 - $s1, 0])
    cylinder(h=$ds, d=$d1);
    
    // LEDs
    //translate([$bx / 2, $r1 + $s1, 0])
    //cylinder(h=$ds, d=$d2);
    //
    //translate([$bx / 2 - 2 * $d2, $r1 + $s1,0])
    //cylinder(h=$ds, d=$d2);
    //
    //translate([$bx / 2 + 2 * $d2, $r1 + $s1,0])
    //cylinder(h=$ds, d=$d2);

    rotate([90,0,90])
    translate([$by/2,$bz,$bx-$ws])
    cylinder(h=$ws,d=3);

    rotate([90,0,90])
    translate([$by/2,$bz,0])
    cylinder(h=$ws,d=3);
}

$ex=60;
$ey=40;
$ez=0.2;

$fx=($bx - $ex)/2;
$fy=($by - $ey)/2;

translate([$fx, $fy, $ds])
rfid($ex, $ey, $ez);
