# Attendance Capture

The Project is About Taking Class Attendance With only a Photo of the Class, it's Based on Computer Vision Methods To Extract The Faces Features in the Image and Detect Who Attended and Who Didn't

## Front Side

Our Front Side is Responsople For Using The Model With Easy User Experince. From uploading the Image And Display The Results, To Downloading the Attendance Sheet Updated

![alt text](https://github.com/omarahmedelnemr/Attendance-Capture/blob/5e118be915c85323d4da61c59f4128445043454e/templates/Webpage%20Preview.png)

### Step 1: Upload The Image

When You Open the Webpage, You Will Find the Upload Button To Upload Your Image to the Server, Then You Have to Type the Code of The Class in Order to Name the Sheet. Then You Press on Detect Faces Button To Start Procceing

![alt text](https://github.com/omarahmedelnemr/Attendance-Capture/blob/5e118be915c85323d4da61c59f4128445043454e/templates/Upload%Image.png)

### Step 2: Results

once You Click, the Server Start Procceing the Uploaded Image, Extratcing the Faces, Detecting each one's Identity, and Then Return images Paths on the Server to Display, and The Label For Each one

![alt text](https://github.com/omarahmedelnemr/Attendance-Capture/blob/5e118be915c85323d4da61c59f4128445043454e/templates/proccessing%Image.png)

![alt text](https://github.com/omarahmedelnemr/Attendance-Capture/blob/5e118be915c85323d4da61c59f4128445043454e/templates/results%Image.png)

### Step 3: Attendance Sheet

Along side with Detetcing the Student Names, The Server take the Class code and Search for a Sheet with the Same name, if Exist, The Server add a New Column With Today's Date, and Then Add the Attendace (0 For Absent, 1 For Attended), if the Files Doesn't Exist, it Create a Copy of The Base File (Called all.csv), Which have the Names and the IDs For All Class Student, And Then name it with the Given Class Code, and Add a Column With Today's Date and Add the Attendance. After All this, The Server Return a Link for this File To The Server To Download the Sheet

### Step 4: Final Step

After Everything is Done, The Front Page Will update the Control Buttons,New Buttons Will Display like: Download The Sheet, Display the Origianl/Annotated Image, Clear The Screen To Test New Image, and So on.

![alt text](https://github.com/omarahmedelnemr/Attendance-Capture/blob/5e118be915c85323d4da61c59f4128445043454e/templates/Sheet%20Image.png)

## Here is The Phase to Get This Magic Done

## Phase 1: Training

### Step 1: Data Collection

First, Each Student Records a 5-second video of showing His/Her Faces Saying Anything. face Rotation, and Words with Mouth Moving Will Be Useful to add Some Variety to The Dataset.
For Each Video, We Extarct n Frames each Second to Convert The Data into a Set of Images for Each Student

### Step 2: Data Cleaning and Preproccessing

After We Extracted the Images From the Video, We Used a Pre-Trained Face Detection Model to extract only Faces From Images to Reduce Noise and Irrelevant Information.
if the Data is Still Small, We perform some Algorethmes on the Images Such as Image augmentation, Image Enhancement, Equalization, Coloring, ..etc. These Algorethmes Will Help To Increase the Dataset Size with Variant Images

### Step 3: Modeling

Once the Dataset is Cleaned, We Are Ready to Train our Model. Since there are a lot of pre-trained Models For General Face Detection, our Purpose is Minimized to Detecting the Face identity, For This Goal, We Will Use a Pre-Trained Model To Encode the Dataset Image And Extract Face Embedings (Face Features), This Step Will Help us in Modeling as We Are no longer Dealing With Images (pixels), We Are Now Dealing With Matrix of Features (Matrix of Numbers Representing The Features) Focusing only on Different Face Features For Each Student.
For This Problem, our Model is a Classification Model, After We Tested Some ML Algorithms Like Support Vector Machine (SVM), Random Forest (RF), and K-Nearest Neighbors (knn), We Chose Support Vector Machine (SVM) with a Linear Kernal, as It returns the Highest Accuracy.

## Phase 2: Testing and Prediction

### Step 1: Data Proccessing

as We Did for "Data Cleaning and Preproccessing", When We Take an Image as Input, We Need To Perfom some Prooccessing in order to make it Fit For our Model To Predict it. It Mainly Does The Same: Read the Image, Extract Faces From This Image, Encode Them To Extract The Face Embeddings (Face Features), Then Biuld a Matrix of all This Faces Embrding in the Image, and We Will Use This as the our input to The Model

### Step 2: Prediction

Now We Have to Feed our Input to the Model, and Let The Model Handle The Magic.
When The We Give Our Data to the Model, the Model Respond with Some Output Number, after That User the Label Encoder, We Decode This Indexes into It's Labels, aka Students Names.
