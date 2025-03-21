

# OCR Project

## Introduction

This project focuses on extracting text from scanned historical documents using three distinct approaches: traditional OCR engines (EasyOCR and Tesseract) and a state-of-the-art language model approach with Google’s Gemini LLM.  
  
Traditional engines like Tesseract and EasyOCR have served well for years, but they often stumble on degraded documents, irregular fonts, and complex layouts. In contrast, Gemini leverages advanced transformer architectures and deep contextual reasoning to deliver impressive accuracy—achieving an average Word Error Rate (WER) of 0.25 and Character Error Rate (CER) of 0.07, compared to 0.78/0.32 for EasyOCR and 0.60/0.19 for Tesseract. Gemini’s multi-modal capabilities let it “see beyond” noise and handle degraded, archaic texts more effectively, though its output may require minimal post-processing for critical applications. 

## Dataset

I use multiple collections of scanned historical documents. These include PDF documents processed into images and paired with ground truth transcriptions . The diversity of document conditions—ranging from well-preserved texts to heavily degraded originals—provides a realistic challenge for comparing OCR methods.

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
      
   - **Google’s Gemini LLM:**  
     Leveraging transformer-based reasoning and a multi-modal input pipeline, Gemini consistently produces near-reference quality outputs. It preserves subtle nuances in historical texts and shows robust performance even on degraded or complex documents. The model’s advanced language understanding allows it to “reason through” errors that stymie traditional OCR engines. It can also filter out irrelevant parts when appropriate prompts.

4. **Text Processing:**  
   Post-processing routines remove diacritical marks (except for ñ) and duplicate white spaces. 

5. **Evaluation:**  
   The performance of each tool is evaluated using Word Error Rate (WER) and Character Error Rate (CER). Detailed metrics are stored in CSV files.

## Results and Comparisons

- **EasyOCR:**  
  Average WER: 0.78 | Average CER: 0.32  
  *Strengths:* Simplicity, multi-language support for many well-structured documents.  
  *Weaknesses:* Struggles with irregular spacing and noisy backgrounds.
  
- **Tesseract:**  
  Average WER: 0.60 | Average CER: 0.19  
  *Strengths:* Good for high-resolution images with proper preprocessing.  
  *Weaknesses:* Sensitive to image skew, lighting variations, and less effective on heavily degraded or complex layouts.
  
- **Google Gemini LLM:**  
  Average WER: 0.25 | Average CER: 0.07  
  *Strengths:* Superior accuracy and consistency across document types; maintains structure and nuance in the extracted text.  
  *Weaknesses:* Although highly accurate, it may be overkill for simpler documents and can be more resource-intensive.

Overall, the results demonstrate that while traditional engines have their place, the advanced reasoning and multi-modal input of Gemini make it particularly well-suited for historical documents where accuracy and preservation of context are paramount.

## Conclusion

The choice of OCR tool depends on the document type and processing requirements:
- **Tesseract** remains a robust solution when images are preprocessed correctly and the document layout is standard.
- **EasyOCR** offers ease-of-use and good performance on cleaner documents but may falter on noisy inputs.
- **Google Gemini LLM** stands out for challenging documents, thanks to its sophisticated reasoning capabilities and multimodal processing—even though it requires slightly more computational resources.

While all three methods have strengths, Gemini’s significant accuracy improvements position it as the future of OCR in contexts where document integrity and nuanced understanding are critical.

## Future Directions

Future improvements could include:
- **Enhanced Preprocessing:**  
  Integrating a fine-tuned CNN for text region detection may further boost accuracy, especially for heavily degraded documents.
  
- **Hybrid Approaches:**  
  Combining the speed of traditional OCR (e.g., Tesseract) with the nuanced understanding of Gemini could yield a hybrid system that uses each engine where it excels.
  
- **Enhanced Postprocessing:**  
  Additional rule-based adjustments can address occasional misrecognitions (e.g., “diffeño” vs. “disseño”) particularly noticeable in Tesseract’s output.
  
- **Multilingual and Script Expansion:**  
  Fine-tuning models for additional languages, especially low-resource scripts, can extend the project’s applicability.



