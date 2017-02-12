#!/usr/bin/env ruby

# format is like this

#  #Q The author of the novel A Portrait of the Artist as a Young Man is this writer.
#  ^ James Joyce
#  A T. S. Eliot
#  B Samuel Beckett
#  C William Faulkner
#  D James Joyce

# use converter like this:
# ruby converter.rb input_file
# this will create an input_file.json
# you can also pass multiple files like so
# ruby converter.rb input_file1 input_file2
# or even like so
# ruby converter.rb folder/*

require 'json'
require 'pathname'

def stripAndEncode(str)
  return str.strip!.force_encoding('ISO-8859-1').encode('UTF-8')
end

ARGV.each do |file|
  if File.directory?(file)
    puts "#{file} is a directory. Skipping."
    next
  end

  questions = []
  question = {}

  File.open(file, "r") do |fh|
    while(line = fh.gets) != nil
      line = stripAndEncode(line)
      if line.start_with?('#Q ')
        question[:question] = line[3..-1]
        question[:category] = Pathname.new(file).basename
        until (line = fh.gets) == nil || line.start_with?('^ ') do
          line = stripAndEncode(line)
          question[:question] << "\n"
          question[:question] << line
        end
        line = stripAndEncode(line)
      end

      if line.start_with?('^ ')
        question[:answer] = line[2..-1]
      elsif ('A '..'Z ').include?(line[0..1])
        question[:choices] ||= []
        question[:choices] << line[2..-1]
      elsif line.empty?
        questions << question unless question.empty?
        question = {}
      end
    end
  end

  File.write("#{file}.json", questions.to_json)
end

