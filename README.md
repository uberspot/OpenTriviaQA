# OpenTriviaQA

A creative commons dataset of trivia, multiple choice questions and answers.

url: [https://github.com/uberspot/OpenTriviaQA](https://github.com/uberspot/OpenTriviaQA)

I searched around some years ago and couldn't find any publicly available dataset of trivia questions so some were 
gathered and split a bit crudely in categories for public usage.

The general format of the files is:

    #Q A question until the newline
    ^ The text of the correct answer
    A multiple choice answer 1
    B multiple choice answer 2
    C multiple choice answer 3
    D ....
    E ...
    .....

A better format could be used in retrospect but a) this one is easy for humans to edit and change questions b) it can be
parsed fairly easy to json or something different later on.

## Contributing

Just fork the project on github, add your changes and send a pull request

Possible contributions can be adding more questions/answers, doing finer categorization, writing a quick parser to
change the files to a better format that is also human friendly.


## License

This work is licensed under the Creative Commons Attribution-ShareAlike 4.0 International License. To view a copy of
this license, visit [http://creativecommons.org/licenses/by-sa/4.0/](http://creativecommons.org/licenses/by-sa/4.0/) .
