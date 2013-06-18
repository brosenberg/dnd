#!/usr/bin/perl -w

use strict;

my $r = qr/([0-9]+\s*x\b\s*)?([0-9]+)\s*(pp|gp|ep|sp|cp)\b\s*(each)?(set)?(\s*;)?/;
my $gold_value = { 'pp' => 10,
                   'gp' =>  1,
                   'ep' => .5,
                   'sp' => .1,
                   'cp' => .10,
                 };
my $total;

while (<>) {
    chomp;
    print;
    s/,//;
    if ( /^pp: / ) {
        /^pp: ([0-9]+) gp: ([0-9]+) ep: ([0-9]+) sp: ([0-9]+) cp: ([0-9]+)/;
        my $val = 10*$1 + $2 + 0.5*$3 + 0.1*$4 + 0.01*$5;
        print " = $val gp\n";
        $total += $val;
        next;
    }
    if ( /$r/ ) {
        print " =";
        while ( /($r)/ ) {
            no warnings;
            $1 =~ /$r/;
            my $val = defined $1?$1*$2:$2;
            if ( defined $gold_value->{$3} ) {
                $val *= $gold_value->{$3};
            }
            print " $val +";
            $total += $val;
            s/$r//;
        }
        print "\bgp";
    }
    print "\n";
}

print "\nTotal: $total gp\n";
