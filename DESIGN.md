RECORDS - How It Was Made


First, the homepage consists of three discs which were made with CSS and look like records.
Making the text fit inside the circles involed creating another, invisible circle that would be
the "text box," allowing the circles to be updated. To update the submissions to the latest
one, I used SQL and organized the records table be date then limited my selection to 1 and
jumped whatever number was adequate to get the first, second, and third-last elements. After
selecting the elements and setting them equal to a variable, it was easy to send that variable
to index.html and use only certain aspects: song, artist, date.

I was not able to get rid of the large amount of space between the vinyls without messing text and
circles, so I created "hyperlinks" that would take you to specific parts of the page. Then I simply
put smooth scroll in CSS that I found on a Youtube video in order to make the transition from vinyl
to vinyl a lot more smoother.


For the "Make a Record" tab, I created a form that would take in all the information that was needed
and then save it to a table called records. I knew that I wanted the user to input every single
element so I attempted to use an apology page but later discovered that by simply putting "required"
at the end of each input, the form would not continue onward unless it was fulfilled.

The "Timeline" table was the most difficult part because of the design. Although it looks simple, I
had a difficult time having the elements align properly and also having all the text fit in the boxes.
This timeline is not hardcoded with the information; but rather, it is updated by a database, so I
decided that the best way to be able to update this table every time after a submission was to create
a loop that would go through every single row and take all the information necessary. I also decided I
wanted the timeline to get thinner as the user scrolled to show how far back they are going. The timeline
outline was one that I found (it has been cited) but because the original timeline had the information
harcoded, I had to out a lot of the code in order to change it into a looped timeline.

