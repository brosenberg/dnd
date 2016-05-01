#!/usr/bin/perl -w

use strict;

my $colors = {};
my $first = 1;

sub color {
    my ($color, $mod) = @_;
    my $c = { 'red'     => 31,
              'green'   => 32,
              'yellow'  => 33,
              'blue'    => 34,
              'purple'  => 35,
              'cyan'    => 36,
              'white'   => 37,
              'reset'   => 0 };
    my $m = { '' => 0, 'bright' => 1, 'dim' => 2 };
    return sprintf("\e[%d;%dm", $m->{"$mod"}, $c->{"$color"});
}

for my $color ( 'red', 'green', 'yellow', 'blue', 'purple', 'cyan', 'white' ) {
    $colors->{"$color"} = &color($color, '');
    for my $mod ( 'bright', 'dim' ) {
        $colors->{"${mod}_$color"} = &color($color, $mod);
    }
}

$colors->{'reset'} = "\e[0m";

while (<>) {
    if ($first) {
        s/^(.*)$/$colors->{'bright_yellow'}-$1-$colors->{'reset'}/igx;
        $first = 0;
    }
    # Stats
    s/(\b
        (
            (Str(ength)?)|
            (Dex(terity)?)|
            (Con(stitution)?)|
            (Wis(dom)?)|
            (Int(ellignce)?)|
            (Cha(risma)?)
        )
        \b)
    /$colors->{'yellow'}$1$colors->{'reset'}/igx;

    # Skills
    s/(\b(
            (Acrobatics)|
            (Animal Handling)|
            (Arcana)|
            (Athletics)|
            (Deception)|
            (History)|
            (Insight)|
            (Intimidation)|
            (Investigation)|
            (Medicine)|
            (Nature)|
            (Perception)|
            (Performance)|
            (Persuasion)|
            (Religion)|
            (Sleight of Hand)|
            (Stealth)|
            (Survival)
        )\b)
    /$colors->{'purple'}$1$colors->{'reset'}/igx;

    s/(\s\+[0-9]+)(,)?(\s)/$colors->{'green'}$1$colors->{'reset'}$2$3/igx;
    s/(\s\-[0-9]+)(,)?(\s)/$colors->{'dim_red'}$1$colors->{'reset'}$2$3/igx;
    s/^(.+::)/$colors->{'blue'}$1$colors->{'reset'}/igx;
    s/^(.+:)/$colors->{'dim_white'}$1$colors->{'reset'}/igx;

    # Numbers
    s/(\s[0-9]+)(,?\s)/$colors->{'cyan'}$1$colors->{'reset'}$2/igx;
    s/^([0-9]+)(,?\s)/$colors->{'cyan'}$1$colors->{'reset'}$2/igx;
    s/(\s[0-9]+)$/$colors->{'cyan'}$1$colors->{'reset'}/igx;
    print;
}
