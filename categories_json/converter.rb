# format is like this

#  #Q The author of the novel A Portrait of the Artist as a Young Man is this writer.
#  ^ James Joyce
#  A T. S. Eliot
#  B Samuel Beckett
#  C William Faulkner
#  D James Joyce

# use converter like this: ruby converter.rb input_file > output.json

require 'json'

questions = []
question = {}

File.readlines(ARGV[0]).each do |line|
  line = line.strip!.force_encoding('ISO-8859-1').encode('UTF-8')
  if line.start_with?('#Q ')
    question[:question] = line[3..-1]
  elsif line.start_with?('^ ')
    question[:answer] = line[2..-1]
  elsif ['A ','B ','C ','D '].include?(line[0..1])
    question[:choices] ||= []
    question[:choices] << line[2..-1]
  elsif line.empty?
    questions << question unless question.empty?
    question = {}
  end
end

puts questions.to_json
