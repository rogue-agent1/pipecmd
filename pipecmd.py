#!/usr/bin/env python3
"""pipecmd - Pipe-friendly data transformation CLI."""
import sys, argparse, re, json, hashlib

def main():
    p = argparse.ArgumentParser(description='Pipe data transformer')
    sub = p.add_subparsers(dest='cmd')
    
    for name in ['upper','lower','title','strip','reverse','sort','uniq','count',
                  'head','tail','grep','replace','split','join','prefix','suffix',
                  'number','dedup','shuffle','hash','length','freq','wrap','unwrap']:
        s = sub.add_parser(name)
        if name in ('head','tail'): s.add_argument('-n', type=int, default=10)
        if name == 'grep': s.add_argument('pattern'); s.add_argument('-v', '--invert', action='store_true')
        if name == 'replace': s.add_argument('old'); s.add_argument('new')
        if name == 'split': s.add_argument('-d', '--delimiter', default=None)
        if name == 'join': s.add_argument('-d', '--delimiter', default=' ')
        if name in ('prefix','suffix'): s.add_argument('text')
        if name == 'hash': s.add_argument('-a', '--algo', default='sha256')
        if name == 'wrap': s.add_argument('-w', '--width', type=int, default=80)
    
    args = p.parse_args()
    if not args.cmd: p.print_help(); return
    
    lines = [l.rstrip('\n') for l in sys.stdin]
    
    if args.cmd == 'upper': lines = [l.upper() for l in lines]
    elif args.cmd == 'lower': lines = [l.lower() for l in lines]
    elif args.cmd == 'title': lines = [l.title() for l in lines]
    elif args.cmd == 'strip': lines = [l.strip() for l in lines]
    elif args.cmd == 'reverse': lines = lines[::-1]
    elif args.cmd == 'sort': lines = sorted(lines)
    elif args.cmd == 'uniq': lines = list(dict.fromkeys(lines))
    elif args.cmd == 'count': print(len(lines)); return
    elif args.cmd == 'head': lines = lines[:args.n]
    elif args.cmd == 'tail': lines = lines[-args.n:]
    elif args.cmd == 'grep':
        pat = re.compile(args.pattern, re.I)
        lines = [l for l in lines if (not args.invert) == bool(pat.search(l))]
    elif args.cmd == 'replace': lines = [l.replace(args.old, args.new) for l in lines]
    elif args.cmd == 'split':
        for l in lines:
            for part in l.split(args.delimiter): print(part)
        return
    elif args.cmd == 'join': print(args.delimiter.join(lines)); return
    elif args.cmd == 'prefix': lines = [args.text + l for l in lines]
    elif args.cmd == 'suffix': lines = [l + args.text for l in lines]
    elif args.cmd == 'number': lines = [f"{i:>4}: {l}" for i, l in enumerate(lines, 1)]
    elif args.cmd == 'dedup':
        seen = set(); result = []
        for l in lines:
            if l not in seen: seen.add(l); result.append(l)
        lines = result
    elif args.cmd == 'shuffle':
        import random; random.shuffle(lines)
    elif args.cmd == 'hash':
        lines = [hashlib.new(args.algo, l.encode()).hexdigest() for l in lines]
    elif args.cmd == 'length': lines = [str(len(l)) for l in lines]
    elif args.cmd == 'freq':
        from collections import Counter
        for val, cnt in Counter(lines).most_common():
            print(f"{cnt:>6}  {val}")
        return
    elif args.cmd == 'wrap':
        import textwrap
        lines = [wrapped for l in lines for wrapped in textwrap.wrap(l, args.width)]
    elif args.cmd == 'unwrap':
        print(' '.join(lines)); return
    
    print('\n'.join(lines))

if __name__ == '__main__':
    main()
