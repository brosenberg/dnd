#!/usr/bin/perl -w

use strict;
use Getopt::Long;
use JSON 2.28;

my $print = 0;

GetOptions('print' => \$print,
           'help'  => sub { print "$0: [input file]\n"; exit 1;}
);

if (! scalar @ARGV) { die "$0: [input file]\n"; }

open(my $FH,'<',"$ARGV[0]") or die "$!\n";

$/ = undef;
my $json = <$FH>;
my $h = decode_json $json;

for my $k ( sort keys %$h ) {
    if ( $print ) {
        print "$k\n";
        &print_weights($h->{$k});
        print "\n";
    } else { 
        printf "%20s: %s\n",$k,&weight_roll($h->{$k});
    }
}
close $FH;

sub weight_roll {
    my ($h) = @_;
    my $total = 0;
    my $weights = {};
    for my $k ( keys %$h ) {
        $weights->{$h->{$k}+$total} = $k;
        $total+=$h->{$k};
    }
    my $roll = int(rand($total))+1;
    for my $k ( sort {$a<=>$b} keys %$weights ) {
        if ( $roll <= $k ) {
            return $weights->{$k};
        }
    }
}

sub print_weights {
    my ($h) = @_;
    my $total = 0;
    for my $k ( keys %$h ) {
        $total+=$h->{$k};
    }
    for my $k ( sort {$h->{$b} <=> $h->{$a}} keys %$h ) {
        printf "%-15s %4.1f%%\n",$k,$h->{$k}/$total*100;
    }
}
