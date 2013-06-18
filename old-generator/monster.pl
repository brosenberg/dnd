#!/usr/bin/perl -w

# This doesn't work completely past the highest cr in $cr_file

# TODO: Calcuate via XP value and not CR value

use strict;
# &encounter() recurses a lot.
no warnings "recursion";


if ( ! scalar @ARGV ) {
    die "Usage: $0 CR [split chance]\n";
}

my $cr_file = "cr-list";
my $template_file = "templates";
my $cr2xp_file = "cr2xp";
my $rand_cr = $ARGV[0];

my $split_chance = 10;
if ( $ARGV[1] ) { $split_chance = $ARGV[1]; }

my $mobs = {};
my $templates = {};
my @cnt_ary = (1,1,2,3,4,6,8,12,16);
my $cr2xp = {};

$mobs->{"max_cr"} = 0;

open(my $CR_FH, "<", "$cr_file") or die "$cr_file: $!\n";
open(my $CR2XP_FH, "<", "$cr2xp_file") or die "$cr2xp_file: $!\n";
open(my $TEMPLATE_FH, "<", "$template_file") or die "$template_file: $!\n";

foreach ( <$CR_FH> ) {
    chomp;
    s/#.*//;
    next if ( /^\s*$/m );
    (my $cr = $_) =~ s/^(.+):.*$/$1/;
    (my $monsters = $_) =~ s/^.+:(.+?)$/$1/;
    foreach my $monster ( split(',',$monsters) ) {
        $monster =~ s/^\s*//; $monster =~ s/\s*$//;
        push(@{$mobs->{"$cr"}},$monster);
    }
    if ( $cr =~ /\//m ) {
        if ( &frac2dec($cr) > $mobs->{"max_cr"} ) {
            $mobs->{"max_cr"} = &frac2dec($cr);
        }
    } elsif ( $cr > $mobs->{"max_cr"} ) {
        $mobs->{"max_cr"} = $cr;
    }
}

foreach ( <$TEMPLATE_FH> ) {
    chomp;
    s/#.*//;
    next if ( /^\s*$/m );
    (my $mod = $_) =~ s/^(.+) .*$/$1/;
    (my $template = $_) =~ s/^.+ (.+?)$/$1/;
    $templates->{"$template"} = $mod;
}

foreach ( <$CR2XP_FH> ) {
    chomp;
    s/#.*//;
    next if ( /^\s*$/m );
    (my $cr = $_) =~ s/^(.+) .*$/$1/;
    (my $xp = $_) =~ s/^.+ (.+?)$/$1/;
    $cr2xp->{"$cr"} = $xp;
}

close $CR_FH;
close $CR2XP_FH;
close $TEMPLATE_FH;

&new_encounter;

sub new_encounter {
    my @encounter;
    my $xp = 0;
    if ( ($rand_cr) > $mobs->{"max_cr"} ) {
        warn "Input CR higher than highest CR monster, setting CR to ",$mobs->{"max_cr"};
        $rand_cr = $mobs->{"max_cr"};
    }
    @encounter = sort cr_sort &encounter($rand_cr,$rand_cr);
    foreach ( @encounter ) {
        $xp += &mob2xp($_);
    }
    
    print "CR $rand_cr encounter:\n\n";
    print "CR Monster\n";
    print join("\n",@encounter),"\n\n";
    print scalar(@encounter)," monster(s)\n";
    printf "XP: %d (%d difference)\n",$xp,&mob2xp("$rand_cr")-$xp;
}

# Pick a random creature of a given CR
sub gen_cr {
    my ($cr) = @_;
    my $mob = @{$mobs->{"$cr"}}[ rand( scalar( @{$mobs->{"$cr"}} )) ];
    return "$cr $mob";
}

# Given an encounter CR, return a list of CRs of the monsters in the encounter
sub encounter {
    my ($cr,$orig_cr) = @_;
    my @retval = ();
    # Maximum difference in CR allowed between a single creature and the encounter's CR
    my $split;
    # Don't split a fractional CR. Force split if encounter CR is higher than highest monster CR. Check random split chance.
    if ( 
         $cr !~ /\//m && 
         ( $cr > $mobs->{"max_cr"} ||
           (rand(100)+1 <= $split_chance ) )
       )
    {
        $split = 1; 
    }

    if ( $split ) {
        my $max_diff = (9-($orig_cr-$cr))%((scalar @cnt_ary)+1);
        if ( $cr > 2 ) {

        # If the CR of the encounter is higher than the highest CR monster, force multiple enemies.
            # Generate a new encounter that is 2 - 8 CR less than the original CR
            # Creatures in an encounter can be at most 10 CR less than the encounter's CR
            my $cr_diff = 1+( (rand($cr-2)+1) % ($#cnt_ary-2) );
            if ( $cr_diff < 2 ) { $cr_diff = 2; }
            if ( $cr_diff > $max_diff ) { $cr_diff = $max_diff; }
            my $cnt = $cnt_ary[$cr_diff];
            foreach ( 1 .. $cnt ) {
                push (@retval, (&encounter($cr-$cr_diff,$orig_cr)));
            }

        } elsif ( $cr == 2 ) {
            my $cnt = (2,4,8)[ int rand(2) ];
            my $new_cr = sprintf("1/%d",$cnt);
            foreach ( 1 .. ($cnt+($cnt/2)) ) {
                push (@retval, (&encounter($new_cr,$orig_cr)));
            }
        } elsif ( $cr == 1 ) {
            my $cnt = (2,3,4,6,8)[ int rand(5) ];
            my $new_cr = sprintf("1/%d",$cnt);
            foreach ( 1 .. $cnt ) {
                push (@retval, (&encounter($new_cr,$orig_cr)));
            }
        } else {
            push (@retval, &gen_cr($cr));
        }

    } else {
        push (@retval, &gen_cr( $cr ));
    }
    return @retval;
}


# Turn fractions into decimal numbers
sub frac2dec {
    my ($cr) = @_;
    if ( $cr =~ /\//m ) {
        (my $num = $cr) =~ s/^(.+)\/.+$/$1/;
        (my $den = $cr) =~ s/^.+\/(.+)$/$1/;
        $cr = $num / $den;
    }
    return $cr;
}

# Sort by CR
sub cr_sort {
    &frac2dec((split(' ',$a))[0]) <=> &frac2dec((split(' ',$b))[0]);
}

# Take in a "CR Monster" string and return the XP value
sub mob2xp {
    my ($mob) = @_;
    my $cr = (split(' ',$mob))[0];
    return $cr2xp->{"$cr"};
}
