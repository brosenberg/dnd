#!/usr/bin/perl -w

use strict;


my $monster_script = "./monster.pl";
my $feature_script = "./feature.pl";

if ( ! @ARGV || ! int $ARGV[0] ) {
    die "Usage: $0 CR\n";
}

my $cr = int $ARGV[0]; 

my $roll = (int rand(100))+1;
my $monster = $roll < 51 ? 1 : 0;
my $minor_f = 0;
my $major_f = 0;
my $treasure = 0;
my $trap = 0;
my $door_cnt = (int rand(4))+1;
my @doors = (
                "simple wooden",
                "simple wooden",
                "simple wooden",
                "good wooden",
                "good wooden",
                "strong wooden",
                "strong wooden",
                "stone",
                "iron",
                "portcullis",
                "secret",
);
my @shape = ( 
                "20'x20'",
                "20'x20'",
                "20'x20'",
                "20'x20'",
                "30'x30'",
                "40'x40'",
                "20'x30'",
                "20'x30'",
                "20'x30'",
                "30'x50'",
                "40'x60'",
                "20'x20'",
                "Unusual",
            );
# Check if there are features, and how many
if (
    ($roll >= 19 && $roll <= 44) ||
    ($roll == 47 ) ||
    ($roll == 48 ) ||
    ($roll >= 50 && $roll <= 79)
   ) {
    $minor_f = (int rand(4))+1;
    $major_f = (int rand(4))+1;
}

# Treasure
if (
    ($roll == 45) ||
    ($roll == 47) ||
    ($roll == 49) ||
    ($roll == 50) ||
    ($roll == 77) ||
    ($roll >= 79 && $roll <= 81 )
   ) {
    $treasure = 1;
}

# Trap
if (
    ($roll == 46) ||
    ($roll >= 48 && $roll <= 50) ||
    ($roll == 78) ||
    ($roll == 79) ||
    ($roll == 81) ||
    ($roll == 82)
   ) {
    $trap = 1;
}

print "\nRoom ($roll) is ",$shape[(int rand(12))+1]," with $door_cnt door(s)\n";
foreach my $door ( 2 .. $door_cnt ) {
    #my $secret = 
        #(int rand(10)) == 
            #5 ? 
                #sprintf (" Secret Door: (DC +%d)",(int rand(3))) 
            #: "";
    #print "Door $door: ",(int rand(100)+1),"$secret\n";
    my $locked = (rand(100) < 3 ) ? 1 : 0;
    if ( $locked ) { print "Locked "; }
    print ucfirst( $doors[ int rand(scalar @doors) ] ), " door\n";
}
if ( $monster ) { 
    if ( defined $cr ) {
        my $monsters = `$monster_script $cr`;
        $monsters =~ s/\n/\n\t/g;
        print "Monsters:\n\t$monsters\n";
    } else {
        print "There is a monster (",(int rand(100))+1,")\n"; 
    }
}
if ( $trap ) { print "There is a trap (DC +",(int rand(3)),")\n"; }
if ( $treasure ) { print "There is a hidden treasure\n"; }
if ( $minor_f ) { print "Features:\n",`$feature_script $minor_f $major_f`,"\n"; }
print "\n";
