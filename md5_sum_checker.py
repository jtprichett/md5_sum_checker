"""
    MD5 sum checker to check files against their checksums
    equating if they are equal.

    Python 2.7.15

    @author     Joshua T. Pritchett <jtpritchett@wpi.edu>
    @copyright  ALAS Lab, 2016
"""
import subprocess
import os
import sys
import getopt

"""
    Writes out information for the checksum comparisons
    to a given test file.

    @param string input_directory   directory being checked
    @param string line              line to be written out

    @reuturn void
"""
def write_out(input_directory, line):
    print 'Writing information for %s directory to checked list file..\r\n' % input_directory
    output_file_name = 'check_lists/%s_checked_list.txt' % input_directory
    output_file = open(output_file_name, 'a')
    output_file.write(write_line)
    output_file.flush()
    output_file.close()
    print 'Writing complete!\r\n'


"""
    Takes in an input directory description for a file that
    has a list of checksums for that directory. Compares the
    list of checksums file for that directory to the master list
    of important files found.

    @param string input_directory   directory that was scanned for all it's checksums

    @return void
"""
def check_checksums(input_directory):
    master_checksums = []

    file_to_check = '%s_list.txt' % input_directory
    number_of_matched_checksums = 0

    with open('md5_master_list.txt', 'r') as f:
      for line in f.readlines():
        master_checksums.append(line.split()[0])

    with open(file_to_check, 'r') as f:
        for line in f.readlines():
            if line.split()[0] in master_checksums:
                number_of_matched_checksums += 1

    write_line = 'There were %d found matching checksums for %s' % (number_of_matched_checksums, input_directory)
    write_out(input_directory, line)

"""
    Generates the checksum list for the given input directory.
    Is affected by option type which can either be:
        master  --  directory that has checksums that should be in the master list
        basic   --  directory to check against for the master checksums

    @param string input_directory   directory that should have the checksums generated
    @param string option_type       option type to check either master, basic

    @return void
"""
def generate_checksum_list(input_directory, option_type):

    output_file = ''

    #Check options based on master and open assocaited file
    if option_type == 'master':
        output_file = open('md5_master_list.txt', 'a')

    if option_type == 'basic':
        file_name = '%s_list.txt' % input_directory
        output_file = open(file_name, 'a')


    #We will be using md5sum checksum command in linux
    bash_command = 'md5sum'

    #Traverse the given directory and generate the checksums for each file
    for root, dirs, files, in os.walk(input_directory, topdown=False):
        for partial_file_name in files:
            #Get the full file name
            test_file = os.path.join(root, partial_file_name)

            #Append full file name for bash command
            bash_command += ' %s' % test_file

            #Open subprocess to run bash command
            try:
                subprocess.Popen(bash_command.split(), stdout=output_file)
            except:
                print 'Could not run the subprocess on that given file\r\n'

    #Close the associated output file
    if output_file != '':
        output_file.close()
"""
    Main function for the checksum checking system

    @param array argv array of input arguements to be parsed from the user

    @return void
"""
def main(argv):
    input_directory = ''
    option_type     = ''

    #Check the input options that should be provided by the user
    try:
        opts, args = getopt.getopt(argv, "h:i:t:", ["help", "idirectory=", "optiontype="])
    except:
        print 'there was an error getting the options\r\n'

    #Make sure there are options
    if opts:
        for opt, arg in opts:
            if opt in ("-h", "--help"):
               print 'python md5sum_checker.py -i <directory_name> or -t <target_file>'
               sys.exit()
            elif opt in ("-i", "--idirectory"):
                input_directory = arg
            elif opt in ("-t", "--optiontype"):
                option_type = arg
    else:
        print 'There were no options to check\r\n'

    #Check the option type for the type of checksum list to generate
    if input_directory != '' and option_type == 'master':
        print 'Generating checksum list for master...\r\n'
        generate_checksum_list(input_directory, option_type)
        print 'Checksum list for master complete!\r\n'

    if input_directory != '' and option_type == 'basic':
        try:
            print 'Generating checksum list for basic...\r\n'
            generate_checksum_list(input_directory, option_type)
            print 'Checksum list for basic complete!'
        except:
            print 'There was an issue with generating the checksum list for master\r\n'
            sys.exit(2)
        try:
            print 'Checking the checksums for the basic directory against master...\r\n'
            check_checksums(input_directory)
            print 'Checksum check complete check the check_lists directory'
        except:
            print 'Could not compare the two files for some reason\r\n'
    else:
        print 'The option type must be either master or basic\r\n'


if __name__ == '__main__':
    main(sys.argv[1:])
