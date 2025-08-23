### Critical Verification Step: Always Verify Complete Video Counts

**AFTER processing each YouTube channel, ALWAYS verify that ALL videos were captured:**

1. **Check the channel directly on YouTube** to see the total number of videos
2. **Compare with the extracted count** in video_data.txt
3. **If counts don't match, re-process with a higher limit**

Example verification process:
```bash
# Check how many videos were actually extracted
wc -l /data/work/dev/daurahtafsir-makro/sunan_daud/Kitab_Name/video_data.txt

# Should match the actual number of videos on the YouTube channel
# If not, re-process with higher --max-videos limit
```

This verification step prevents the historical issue where Kitab Jihad only had 50 of its 131 videos.

### Common Issues and Solutions

1. **Incomplete Video Extraction**
   - **Issue**: Only partial videos extracted due to low --max-videos limit
   - **Solution**: Always use --max-videos 500 and verify counts match YouTube

2. **Kitab Not Clickable**
   - Check that kitab name in `kitabList` exactly matches the JavaScript condition
   - Check that directory name matches (spaces to underscores)
   - Check that `index.html` exists in kitab directory
   - Check that JavaScript handler creates an `<a>` element with correct `href`

3. **Spelling Issues**
   - Ensure consistent spelling between `kitabList` and JavaScript conditions
   - Use exact kitab names as they appear on YouTube

4. **Directory Issues**
   - Use underscores instead of spaces in directory names
   - Ensure directory names match kitab names (Kitab Name -> Kitab_Name)

This permanent process ensures that all kitabs are properly implemented and clickable.