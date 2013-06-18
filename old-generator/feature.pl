#!/usr/bin/perl -w

use strict;

my $prog_name = eval{(caller)[1]};

my $major_f = "major-features";
my $minor_f = "minor-features";

open (my $MAJFH, "<", "$major_f") or die "$!";
open (my $MINFH, "<", "$minor_f") or die "$!";

my @major = <$MAJFH>;
my @minor = <$MINFH>;

close $MAJFH;
close $MINFH;

@major = map ucfirst(),@major;
map chomp, @major;
@minor = map ucfirst(),@minor;
map chomp, @minor;

if ( scalar @ARGV != 2 ) {
    die "Usage: $prog_name [Minor Feature Count] [Major Feature Count]\nex: $prog_name 2 3\n";
}

print "\tMinor: ";
foreach ( 2 .. $ARGV[0] ) {
    print $minor[int rand(scalar @minor)],", ";
}
print $minor[int rand(scalar @minor)],"\n";
print "\tMajor: ";
foreach ( 2 .. $ARGV[1] ) {
    print $major[int rand(scalar @major)],", ";
}
print $major[int rand(scalar @major)];
