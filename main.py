import musicpy as mp
import random as rn
from math import gcd
from numpy import char as ch
# Part One: Four Chord Loop Pad Generator
chordtypes = ['M7', 'm7', '7']
distribution = [0]*3 + [-2, -1, 1, 2]
randfirst = (mp.get_chord(mp.degree_to_note(rn.randint(43, 56)), rn.choice(chordtypes)) % (1, 1/2))
chordloop = [mp.chord(randfirst)]
for n in range(0, 3):
    chordn = mp.chord(chordloop[n])
    for i in range(0, 4):
        chordn += (rn.choice(distribution), i)
    chordloop.append(chordn)
piece1 = (chordloop[0] | chordloop[1] | chordloop[2] | chordloop[3]) * 15
# Part Two, Randomized Tone Rows:
tonerows = mp.chord([])
for n in range(0, 4):
    rowshuffle = chordloop[n].notes
    rn.shuffle(rowshuffle)
    for m in range(0, 4):
        tonerows = tonerows | mp.chord([rowshuffle[m]], [1/8])
    rn.shuffle(rowshuffle)
    for m in range(0, 4):
        tonerows = tonerows | mp.chord([rowshuffle[m]], [1/8])
tonerows *= 16
# Part Three, Euclidean Drum Beats:

# copied from https://github.com/WilCrofter/Euclidean_Rhythms/blob/master/euclidean_rhythms.py

def bjorklund(k, n):
    """ Using Bjorklund's algorithm as described in [The Distance Geometry of Music](https://arxiv.org/abs/0705.4085v1),
    return a list of 1's and 0's representing a "Euclidean Rhythm" of k beats and n-k rests.
    """
    if not type(k) == type(n) == int:
        raise TypeError('Arguments must be integers.')
    if not n > k:
        raise ValueError('Second argument must exceed the first.')
    d = gcd(k, n)
    k1 = int(k/d)
    n1 = int(n/d)
    tmp = [[1] for _ in range(k1)] + [[0] for _ in range(n1-k1)]
    while ([0] in tmp) or (len(tmp) > 1):
        idx = tmp.index(tmp[-1])
        if len(tmp) == 1+idx:
            break
        for i in range(min(idx, len(tmp)-idx)):
            tmp[i] += tmp[-1]
        tmp = tmp[0:max(idx, len(tmp)-idx)]
    tmp2 = []
    for i in range(len(tmp)):
        tmp2 += tmp[i]
    ans = []
    for i in range(d):
        ans += tmp2
    return ans


eucrhythm1 = bjorklund(rn.randrange(8, 28), 32)
snarerhythm = mp.get_chords_from_rhythm(mp.N('C5'),
                                        mp.rhythm(' '.join(ch.replace([str(x) for x in eucrhythm1], '1', 'b')), 2)) * 13
eucrhythm2 = bjorklund(rn.randrange(4, 12), 32)
bassrhythm = mp.get_chords_from_rhythm(mp.N('C5'),
                                       mp.rhythm(' '.join(ch.replace([str(x) for x in eucrhythm2], '1', 'b')), 2)) * 14
# Part Four, Print and write the piece!
print(bassrhythm)
piecetoplay = mp.P([tonerows, piece1, snarerhythm, bassrhythm],
                   ['Orchestral Harp', 'Pad 2 (warm)', 'Synth Drum', 'Woodblock'], 150, [0, 4, 8, 12])

mp.write(piecetoplay)
