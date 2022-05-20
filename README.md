# uwgui_flask

The web-based flask version of uwgui supports annotations with points, bounding boxes, and custom shapes, all of which are saved in .csv files. Bounding box and point data contain min/max x/y data and custom shapes yeild bit masks on the basis of a single class. 

### Usage
Move between images using the right and left arrows on the top of the screen. 
Download desired annotations before changing the image. Do not click the download button if no annotations are made on an image. 
Return to the image upload screen with the red exit button on the top righthand side. No data will be saved when exiting. 

#### Uploading Images
The initial screen prompts for file upload. Multiple images can be selected and submitted here. 

### Annotation
Select an annotation format in the *Options* in the upper lefthand corner. 
After completing the annotation on the displayed image, a box will pop up within it's respective category on the left hand side.  <br/><br/>
To delete the annotation, click the red minus button beside the box of the corresponding annotation id. 
Annotation data is not saved between images - moving on to the next or previous image will delete the current annotations, so they must be downloaded to be preserved.

#### Box/Point Annotation
- Click the **Draw Box or Point** button to start an annotation. 
- Click anywhere on the image to annotate a point. Hold down your mouse and drag to annotate a bounding box. 
- The id of these annotations will be visible on the image. 

#### Custom Shape Mask Annotation
- Click the **Draw Custom Shape** button to start an annotation. 
- Every click made on the image represents the vertices of the desired shape. 
- Line segments will connect the points as they are made. Finish the shape by clicking back on the starting point. 
- Multiple custom shapes can be drawn on one image. The image will yield one mask that includes all of the shapes.


