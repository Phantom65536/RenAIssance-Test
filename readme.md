# RenAIssance: OCR for historical documents

## Introduction

This project focuses on extracting text from scanned historical documents using three distinct approaches: traditional OCR engines (EasyOCR and Tesseract), transformer-based models (TrOCR and DONUT), and a state-of-the-art language model approach with Google’s Gemini LLM. The traditional OCR and language model approaches are implemented in `Script.ipynb`, while the transformer-based model approach is in `Script_cropped.ipynb`. Traditional engines like Tesseract and EasyOCR have long been reliable but struggle with degraded documents, irregular fonts, and complex layouts, while transformer-based models like TrOCR and DONUT use encoder-decoder architectures for improved contextual correction and layout analysis, though they require extensive fine-tuning to effectively handle the noise and complexity of historical texts; meanwhile, Gemini leverages advanced transformer architectures and multi-modal reasoning to achieve impressive accuracy.

## Dataset

I used the provided scanned historical documents, converting the PDF files into images paired with ground truth transcriptions. Most documents were split into individual lines to create training and testing samples for the TrOCR model. The `test_sources` folder contains all original PDF files, `extracted_imgs` holds cropped images of the main text, and `cropped_imgs` includes cropped lines from each page. For fine-tuning, `train_data` and `test_data` are created by splitting `cropped_imgs`, while `pdf_labels` store the corresponding ground truth sentences.

## Implementation

The project implementation consists of several stages:

1. **PDF to Image Conversion:**  
   PDF documents are converted into high-resolution images using the `pdf2image` library. Proper preprocessing is essential; images must be scaled so the text’s x-height is at least 20 pixels, and any skew or noise should be corrected to maximize OCR accuracy. 

2. **Main Text Capturing:**  
   An adaptive thresholding algorithm analyzes the average pixel intensity along the horizontal axis to isolate main text regions. This reduces interference from background artifacts and improves the recognition accuracy across all OCR engines.

3. **Text Extraction:**  
   Three OCR tools are applied:
   - **EasyOCR:**  
     Known for its simplicity and multi-language support via a CNN-RNN architecture, EasyOCR works best on clean, organized documents like receipts or well-structured PDFs. However, its performance can drop on noisy, irregular scans. 
   - **Tesseract:**  
     A mature, open-source engine that uses LSTM networks (since version 4) combined with traditional techniques. It performs well on high-resolution, preprocessed images but may introduce character substitutions and layout errors if the input is not optimal.
   - **TrOCR:**  
     It combines a ViT-based image encoder with an autoregressive text Transformer decoder. It yields superior performance across print, handwriting, and scene text tasks.
   - **TrOCR Finetuning:**
     In our fine-tuning experiment, only the first 3 pages of a 5-page document were used. These 3 pages were manually split into individual lines to serve as training samples; the first two pages were used for training and the third page for testing. This approach leverages the base model’s capability to understand Spanish, but highlights the need for further segmentation and more training data to effectively capture historical text nuances.     
   - **DONUT:**  
    It is an OCR-free end-to-end model that uses a Swin Transformer encoder to directly processes the document image, and a transformer decoder to generates the document text or desired fields. The model can learn to handle noisy text, layout, and even some language context all at once. Donut can be fine-tuned to produce plain text transcripts, but it is more complex to train from scratch than fine-tuning TrOCR with synthetic documents.
   - **Google’s Gemini LLM:**  
     Leveraging transformer-based reasoning and a multi-modal input pipeline, Gemini consistently produces near-reference quality outputs. It preserves subtle nuances in historical texts and shows robust performance even on degraded or complex documents. The model’s advanced language understanding allows it to “reason through” errors that stymie traditional OCR engines. It can also filter out irrelevant parts when appropriate prompts.

4. **Text Processing:**  
   Post-processing routines remove diacritical marks (except for ñ) and duplicate white spaces. 

5. **Evaluation:**  
   The performance of each tool is evaluated using Word Error Rate (WER) and Character Error Rate (CER). Detailed metrics are stored in CSV files.

## Results and Comparisons

- **EasyOCR:**  
  Average WER: 0.78 | Average CER: 0.32 (Outputs for provided documents are saved in `easyocr_result_full`)
  *Strengths:* Simplicity, multi-language support for many well-structured documents.  
  *Weaknesses:* Struggles with irregular spacing and noisy backgrounds.
- **Tesseract:**  
  Average WER: 0.60 | Average CER: 0.19 (Outputs for provided documents are saved in `tesseract_result_full`) 
  *Strengths:* Good for high-resolution images with proper preprocessing.  
  *Weaknesses:* Sensitive to image skew, lighting variations, and less effective on heavily degraded or complex layouts.
- **TrOCR:**  
  Average WER: 0.86 | Average CER: 0.65 (Outputs for provided documents are saved in `gemini_result_full`) 
  *Strengths:* Able to handle diverse text styles and contextual error correction.  
  *Weaknesses:* Its generic synthetic pretraining data may not fully capture the nuances of 17th-century Spanish fonts.
- **TrOCR Finetuned:**
  The fine-tuning experiment did not yield satisfactory results. Two main issues were identified. The limited amount of training data (only 3 pages) greatly differed from the model’s original pretraining data. Also, excessive noise and blurriness in the input data hindered performance, even after applying basic image preprocessing techniques like Gaussian blur and adaptive thresholding. These observations suggest that building a dedicated segmentation model for extracting text regions from the noisy documents may be necessary to improve performance in this context.
- **DONUT:**  
  Average WER: 0.94 | Average CER: 0.85  
  *Strengths:* It processes document images directly, capturing both text and layout information to minimize error propagation.  
  *Weaknesses:* It requires extensive fine-tuning for domain-specific layouts, and errors in layout analysis can affect transcription quality.
- **Google Gemini LLM:**  
  Average WER: 0.25 | Average CER: 0.07  
  *Strengths:* Superior accuracy and consistency across document types; maintains structure and nuance in the extracted text.  
  *Weaknesses:* Although highly accurate, it may be overkill for simpler documents and can be more resource-intensive.

Overall, the results demonstrate that while traditional engines have their place, the advanced reasoning and multi-modal input of Gemini make it particularly well-suited for historical documents where accuracy and preservation of context are paramount.

## Conclusion

The choice of OCR tool depends on the document type and processing requirements:
- **Tesseract** remains a robust solution when images are preprocessed correctly and the document layout is standard.
- **EasyOCR** offers ease-of-use and good performance on cleaner documents but may falter on noisy inputs.
- **TrOCR:** and **DONUT:** require extensive fine-tuning to capture the nuances of 17th-century Spanish fonts, especailly with synthetic data and image augmentation.
- **Google Gemini LLM** stands out for challenging documents, thanks to its sophisticated reasoning capabilities and multimodal processing—even though it requires slightly more computational resources.

While all three methods have strengths, Gemini’s significant accuracy improvements position it as the future of OCR in contexts where document integrity and nuanced understanding are critical.

## Future Directions

Future improvements could include (take a look at the proposal for more details):

- **Enhanced Image Preprocessing:**  
  Further improvement in OCR performance could be achieved by exploring advanced image preprocessing techniques tailored to historical documents. Combining traditional image processing with modern CNN-based segmentation can create a robust preprocessing pipeline that maximizes the quality of input images before OCR.
  
- **Hybrid Approaches:**  
  A hybrid OCR system could combine the speed of traditional engines like Tesseract for high-quality regions with the nuanced understanding of Gemini for challenging areas, using dynamic routing and ensemble methods to optimize overall accuracy.
  
- **Enhanced Postprocessing:**  
  Even with improved OCR models, occasional errors—such as misrecognized characters or subtle layout issues—may still occur. To address these, additional rule-based postprocessing can be implemented.
