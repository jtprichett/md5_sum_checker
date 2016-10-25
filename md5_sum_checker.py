import subprocess
import os
import sys
import getopt


def check_checksums(input_directory):
    master_checksums = []
    file_to_check = '%s_list.txt' % input_directory

    output_file_name = 'check_lists/%s_checked_list.txt' % input_directory
    output_file = open(output_file_name, 'a')

    number_of_matched_checksums = 0

    with open('md5_master_list.txt', 'r') as f:
      for line in f.readlines():
        master_checksums.append(line.split()[0])

    with open(file_to_check, 'r') as f:
        for line in f.readlines():
            if line.split()[0] in master_checksums:
                number_of_matched_checksums += 1

    write_line = 'There were %d found matching checksums for %s' % (number_of_matched_checksums, input_directory)
    output_file.write(write_line)
    output_file.flush()
    output_file.close()

def generate_checksum_list(input_directory, option_type):

    output_file = ''

    if option_type == 'master':
        output_file = open('md5_master_list.txt', 'a')

    if option_type == 'basic':
        file_name = '%s_list.txt' % input_directory
        output_file = open(file_name, 'a')

    bash_command = 'md5sum'
    for root, dirs, files, in os.walk(input_directory, topdown=False):
        for partial_file_name in files:
            test_file = os.path.join(root, partial_file_name)
            print test_file
            bash_command += ' %s' % test_file
            print bash_command
            try:
                subprocess.Popen(bash_command.split(), stdout=output_file)
            except:
                print 'could not open the file'

    if output_file != '':
        output_file.close()

def main(argv):
    input_directory = ''
    option_type     = ''
    print argv
    try:
        opts, args = getopt.getopt(argv, "h:i:t:", ["help", "idirectory=", "optiontype="])
    except:
        print 'there was an error'

    if opts:
        for opt, arg in opts:
            if opt in ("-h", "--help"):
               print 'python md5sum_checker.py -i <directory_name> or -t <target_file>'
               sys.exit()
            elif opt in ("-i", "--idirectory"):
                input_directory = arg
            elif opt in ("-t", "--optiontype"):
                option_type = arg

    print option_type
    print input_directory
    if input_directory != '' and option_type == 'master':
        generate_checksum_list(input_directory, option_type)
    if input_directory != '' and option_type == 'basic':
        generate_checksum_list(input_directory, option_type)
        check_checksums(input_directory)
    else:
        print 'Those options are invalid'


if __name__ == '__main__':
    main(sys.argv[1:])
