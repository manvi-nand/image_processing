<p>In this project we are comparing 2 images.</p>
<br>
<p>The input data is in the form of pdfs. These pdf documents first have to be converted to images that is BGR format and then the proessing of the images is done.</p>
<br>
<p>The pdfs are converted to BGR format by using a library called PyMuPDF (fitz)</p>
<br>
<p>After the conversion the absolute pixal-wise intensity difference is found between the two images using the OpenCV library called absdiff().
By creating a difference image we can easily identify where the pixal values are significiently different. This is essential for detecting changes between the 2 images.
Then thresholding and contouring of the difference image is performed (these are come of the basic pre-processing steps).
A loop is created to check if there are any matching contours and to compare the shapes of the two contours. 
The orginal image (image1) and the highlighted image are combined that is blended. The main purpose of the blending is to overlay the highlighted
differnce on top of the orginal image, making it visually clear were the differences are.
At the end this blended image is saved into a seperate folder and the differences between the images can be analyzed</p>
