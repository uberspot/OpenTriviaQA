# EDITED WITH OpenAI's GPT 4-o / o3-high

#!/usr/bin/env ruby
require 'json'
require 'pathname'

# safe `.strip` + ISO-8859-1 → UTF-8
def strip_and_encode(line)
  return '' if line.nil?
  s = line.strip
  s.force_encoding('ISO-8859-1').encode('UTF-8', invalid: :replace, undef: :replace, replace: '')
end

grouped = {}

ARGV.each do |file|
  next if File.directory?(file)
  category = Pathname.new(file).basename.to_s
  grouped[category] ||= []

  current = nil

  File.foreach(file, encoding: 'ISO-8859-1') do |raw|
    line = strip_and_encode(raw)

    case line
    when /\A#Q\s+(.*)/
      # push last question, start new
      grouped[category] << current if current
      current = { "question" => $1.dup, "choices" => [] }
    when /\A\^\s+(.*)/
      current && current.merge!("answer" => $1)
    when /\A([A-Z])\s+(.*)/
      current && current["choices"] << $2
    when ''  # blank line ends a question
      if current
        grouped[category] << current
        current = nil
      end
    else
      # continuation of a multi-line question
      current && current["question"] << "\n" << line
    end
  end

  # push last if file didn’t end with a blank
  grouped[category] << current if current
end

# write out a single JSON file your json2sql.py can load with `data.items()`
File.open('grouped_questions.json','w') do |f|
  f.write JSON.pretty_generate(grouped)
end
