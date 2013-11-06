#!/usr/bin/perl -w
# wget https://spreadsheets.google.com/pub?key=0Ak-IxjmMq9NMdG83a3pOQ1hKTVllVDhISlJmbFJRQ1E&single=true&gid=0&output=csv
use strict;

my $TRAITDB = "/home/ben/Downloads/Traits.csv";
if (!defined $ARGV[0]) {die};
open (my $FH, '<', $TRAITDB) or die "$0: $TRAITDB: $!";

while (<$FH>) {
    if (/$ARGV[0]/i) {
        my @l = split(',');
        map {s/^\s*"?(.+?)"?\s*$/$1/} @l;
        my $s = sprintf("[1;33m%s[0m [1;34m(%s)[0m: %s",$l[0],$l[1],join(', ',@l[5..$#l-2]));
        if (length($ARGV[0])) {
            $s =~ s/($ARGV[0])/[1;31m$1[0m/gi;
        }
        $s =~ s/\s\s+/ /g;
        print "$s\n";
    }
}
close $FH;
