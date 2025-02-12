: Clone your original repository
call git clone https://github.com/jfranmatheu/Blender-ACK.git new-project

: Change into the new directory
cd new-project

: Remove the old origin
call git remote remove origin

: Add the new repository as origin
call git remote add origin https://github.com/username/new-project.git

: Add the original repository as upstream
call git remote add upstream https://github.com/jfranmatheu/Blender-ACK.git

: Push to your new repository
call git push -u origin main
