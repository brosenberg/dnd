#!/usr/bin/perl -w

use strict;

for my $in_file (<*.in>) {
    (my $out_file = $in_file) =~ s/\.in$/.json/;
    open (my $IN, '<', $in_file) or next;
    open (my $OUT, '>', "../$out_file") or next;
    my $h = {};
    my $name = <$IN>;
    chomp $name;
    print $OUT "{\n\t\"$name\":{\n";
    while (<$IN>) {
        chomp;
        /^([0-9]+)–([0-9]+)\s*(.+?)\s+([0-9]+)$/;
        my @ary = ($1, $2, $3, $4);
        if ( !defined $ary[0] || !defined $ary[1] ||
             !defined $ary[2] || !defined $ary[3] ) {
            next;
        }
        printf $OUT ("\t\t\"%s (Avg. CR %d)\":%d", $ary[2], $ary[3], $ary[1]-$ary[0]+1);
        if (!eof) { print $OUT ","; }
        print $OUT "\n";
    }
    print $OUT "\t}\n}\n";
    close $IN;
    close $OUT;
}
