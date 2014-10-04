#!/usr/bin/perl -w

use strict;

for ( split(',', join('',@ARGV) ) ) {
    if ( /^([0-9]+)\s*d\s*([0-9]+)\s*([-+\/*])?\s*([0-9]+)?\s*$/ ) {
        my $mod = defined $3 && defined $4 ? "$3$4" : undef;
        printf "%9s: ", sprintf "%sd%s%s", $1,$2,defined $mod?$mod:'';
        &roll($1,$2,$mod);
    } else {
        warn "I don't understand: $_\n";
    }
}

sub roll {
    my ($die, $sides, $mod) = @_;
    my $total=0;
    my @rolls;
    if ( defined $die && defined $sides ) {
        while ($die--) {
            push @rolls, int(rand($sides))+1;
            $total += $rolls[-1];
        }
        print "(", join('+',@rolls), ")";
        if ( defined $mod ) {
            print "$mod";
            $total = eval "$total$mod";
        }
    }
    print " = $total\n";
}
