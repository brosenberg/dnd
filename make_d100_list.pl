#!/usr/bin/perl -w

use strict;

my @ary;
my $count = 1;

while (<>) {
    chomp;
    push(@ary, $_);
}

my $mult = length(sprintf("%d", scalar @ary));
my $die_size = 10**$mult;
my $inc = ($die_size/(scalar @ary))-1;

print "Roll 1d$die_size\n";
foreach my $entry (@ary) {
    my $dice = "";
    if (int($count) == int($count+$inc)) {
        $dice = sprintf("%d", int($count));
    } else {
        $dice = sprintf("%d - %d", int($count), int($count+$inc))
    }
    &print_dice($dice, $entry);
    $count += $inc+1;
}

if (int($count) <= $die_size) {
    my $entry = "Roll twice";
    my $dice = sprintf("%d - %d", int($count), $die_size);
    if (int($count) == $die_size) {
        $dice = int($count);
    }
    &print_dice($dice, $entry);
}

# Amazing weird Perl format crap.
# http://perldoc.perl.org/perlform.html
sub print_dice {
    no warnings;
    my ($dice, $entry) = @_;
    my $format = sprintf("format STDOUT =\n@%s @*\n%s, %s\n.\n",
                    '|'x(($mult*2)+5), '$dice', '$entry');
    eval $format;
    write;
}
