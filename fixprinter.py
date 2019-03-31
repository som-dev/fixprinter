#!/usr/bin/python3
# requires the python quickfix library: pip (or pip3) install quickfix

import argparse
import quickfix as fix
import sys

# adjust this higher if you expect user-defined tags
MAX_FIX_TAG = 10000


def print_group(prefix, tag, groupCount, fieldMap, dd):
    fieldName = dd.getFieldName(tag, '')[0]
    if not fieldName:
        fieldName = 'Unknown'
    print('{}{} ({}): count = {}'.format(prefix, fieldName, tag, groupCount))
    for num in range(1, groupCount+1):
        group = fieldMap.getGroupRef(num, tag)
        if num > 1:
            print(prefix + '  ----')
        print_fieldmap(prefix + '  ', group, dd)


def print_field(prefix, field, dd):
    tag = field.getTag()
    value = field.getString()
    name = 'Unknown'
    if dd.hasFieldValue(tag):
        name = dd.getValueName(tag, value, '')[0]
        if not name:
            name = 'Unknown'
        value = '{} ({})'.format(name, value)
    fieldName = dd.getFieldName(tag, '')[0]
    if not fieldName:
        fieldName = 'Unknown'
    print('{}{} ({}): {}'.format(prefix, fieldName, tag, value))


# Cannot seem to iterate FieldMap, nor use the iterator
# provided by the FieldMap::begin() method, so brute force
# check each tag here.  May have to adjust tag upper limit
# for custom tag support.
# TODO: Update this to use a proper iterator!
def print_fieldmap(prefix, fieldMap, dd):
    found = 0
    # Here's the brute-force part
    for tag in range(0, MAX_FIX_TAG):
        try:
            field = fieldMap.getFieldRef(tag)
        except fix.FieldNotFound:
            continue  # no field found for the tag so move on
        # we have a field, print it as a group or individual
        groupCount = fieldMap.groupCount(tag)
        if groupCount > 0:
            print_group(prefix, tag, groupCount, fieldMap, dd)
        else:
            print_field(prefix, field, dd)
        found += 1
        if found == fieldMap.totalFields():
            break  # short-circuit the brute-force


def print_msg(msg, dd):
    print_fieldmap('', msg.getHeader(), dd)
    print_fieldmap('', msg, dd)
    print_fieldmap('', msg.getTrailer(), dd)


def create_datadictionary(spec):
    if not spec:
        return fix.DataDictionary()
    else:
        return fix.DataDictionary(spec)


def process_line(line_num, line):
    # within each line we are looking for a start and end:
    #   start should be '8=FIX'...
    #   end should be last SOH character separator '\x01'
    msg = line[line.find('8=FIX'):line.rfind('\x01')+1]
    if not msg:
        return False
    msg_bars = msg.replace('\x01', '|')
    print('\nFound FIX message at line {}: {}\n'.format(line_num, msg_bars))
    msg = fix.Message(msg, dd)
    print_msg(msg, dd)
    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='A pretty printer of fix messages '
                    'using the quickfix library '
                    '(Must specify either --filename or --stdin)')
    parser.add_argument(
        '-f', '--filename', dest='filename', default='',
        help='a file containing fix messages to display')
    parser.add_argument(
        '--stdin', dest='stdin', action='store_true', default=False,
        help='read lines from stdin instead of a file')
    parser.add_argument(
        '--spec', dest='spec', default='',
        help='loads the provided XML specification '
             '(presumably from the quickfix library) '
             'WARNING! The output will be fairly useless without a spec')
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)
    args = parser.parse_args()
    dd = create_datadictionary(args.spec)

    line_num = 1
    messagesFound = 0

    if not args.stdin and not args.filename:
        parser.print_help(sys.stderr)
        sys.exit(1)

    if args.stdin:
        for line in sys.stdin:
            if process_line(line_num, line):
                messagesFound += 1
            line_num += 1
    if args.filename:
        with open(args.filename) as fp:
            for cnt, line in enumerate(fp):
                if process_line(line_num, line):
                    messagesFound += 1
                line_num += 1

    print()
    if messagesFound > 0:
        print('Found {} messages'.format(messagesFound))
    else:
        print('No messages found')
