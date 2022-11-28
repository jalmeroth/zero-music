module standoff($h, $d1, $d2) {
    difference() {
        cylinder(h=$h, d=$d1);
        cylinder(h=$h, d=$d2);
    }
}
