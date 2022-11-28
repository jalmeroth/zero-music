include<standoff.scad>;

module rfid($x=60,$y=40,$z=0.2) {
    // Platte
    color("red")
    cube([$x,$y,$z]);

    // Standoff
    $h=5;  
    $d=6;
    $r=$d/2;
    $s=2.8;     // Loch

    translate([$r+12.5,$r,$z])
    standoff($h,$d,$s);
    translate([$r+12.5,$y-$r-0.5,$z])
    standoff($h,$d,$s);
    translate([$x-$r-5,$y-$r-4.5,$z])
    standoff($h,$d,$s);
    translate([$x-$r-5,$r+5,$z])
    standoff($h,$d,$s);
}
