#!/usr/bin/perl -w
use strict;

my $TRAITDB = "/home/ben/Downloads/Traits.csv";
if (!defined $ARGV[0]) {die};
open (my $FH, '<', $TRAITDB) or die "$0: $TRAITDB: $!";

while (<$FH>) {
    if (/$ARGV[0]/) {
        my @l = split(',');
        my $s = sprintf("[1;33m%s[0m: %s\n",$l[0],join(',',@l[5..$#l-2]));
        $s =~ s/($ARGV[0])/[1;31m$1[0m/gi;
        $s =~ s/\s\s+/ /g;
        print $s;
    }
}
close $FH;
