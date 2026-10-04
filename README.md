# Image Steganography

## 1. Introduction

Image steganography is a technique used to hide secret information inside an image in such a way that the existence of the hidden information is difficult to notice.

Unlike encryption, which makes the message unreadable, steganography focuses on **hiding the existence of the message**.

In this project, secret information is embedded inside an image and can later be extracted using the corresponding extraction process.

---

## 2. How Image Steganography Works

A digital image consists of pixels. Each pixel contains color information, usually represented using RGB (Red, Green, and Blue) values.

For example:

```text
Pixel = (R, G, B)

R = 101
G = 150
B = 200
```

Each color value is stored using binary data.

Steganography can modify the least significant bits of these values to store secret information.

Example:

```text
Original pixel value:
10110110

Modified pixel value:
10110111
```

Only the least significant bit has changed, so the visual difference is usually very small.

---

## 3. Least Significant Bit (LSB) Method

The **Least Significant Bit (LSB)** method is one of the simplest techniques used for image steganography.

The least significant bit is the rightmost bit of a binary number.

Example:

```text
Binary value: 10110110
                         ↑
                       LSB
```

To hide data, selected LSBs of image pixel values are replaced with bits from the secret message.

### Example

Secret character:

```text
A
```

ASCII value:

```text
65
```

Binary representation:

```text
01000001
```

These bits can be embedded into the LSBs of selected pixel values.

---

## 4. Encoding Process

The general encoding process is:

```text
Secret Message
       ↓
Convert message to bytes
       ↓
Convert bytes to binary
       ↓
Read image pixels
       ↓
Modify selected LSBs
       ↓
Generate stego image
```

The resulting image is called a **stego image**.

### Example

```text
Original Image
      +
Secret Message
      ↓
Steganography Algorithm
      ↓
Stego Image
```

---

## 5. Decoding / Extraction Process

The extraction process reverses the embedding operation.

```text
Stego Image
     ↓
Read pixel values
     ↓
Extract LSBs
     ↓
Group bits into bytes
     ↓
Convert bytes to characters
     ↓
Recover Secret Message
```

The extracted message should match the original hidden message when the correct extraction method and parameters are used.

---

## 6. Image Types

Image formats can affect steganography.

### Lossless Formats

Examples:

* PNG
* BMP

Lossless formats preserve the stored pixel information and are therefore generally suitable for basic LSB steganography.

### Lossy Formats

Example:

* JPEG

JPEG compression can modify pixel data and may destroy or alter information stored using simple LSB techniques.

Therefore, this project primarily uses lossless image formats such as **PNG**.

---

## 7. Capacity

An image has a limited amount of space available for hiding information.

For an RGB image:

```text
Width × Height × 3
```

represents the number of color-channel values.

If one bit from each channel is used, the theoretical capacity is approximately:

```text
Width × Height × 3 bits
```

However, the actual usable capacity depends on the implementation and any additional information stored by the application.

### Example

For an image of:

```text
100 × 100 pixels
```

There are:

```text
100 × 100 × 3 = 30,000 color-channel values
```

Using one LSB from each channel gives a theoretical capacity of:

```text
30,000 bits
```

which is approximately:

```text
3,750 bytes
```

---

## 8. Advantages

* Simple to implement.
* Can hide information inside normal-looking images.
* Does not significantly change the appearance of the image when small amounts of data are embedded.
* Can be combined with encryption for stronger protection.
* Useful for learning about digital images, binary data, and information hiding.

---

## 9. Limitations

* The image has limited hiding capacity.
* Excessive modification can introduce detectable changes.
* Simple LSB techniques can be vulnerable to steganalysis.
* Lossy image compression can damage hidden information.
* Re-saving or modifying the image may destroy the embedded data.
* Steganography alone does not provide strong confidentiality.

---

## 10. Steganography vs Encryption

| Feature                   | Steganography               | Encryption                       |
| ------------------------- | --------------------------- | -------------------------------- |
| Main purpose              | Hide the existence of data  | Protect the content of data      |
| Output                    | Looks like an ordinary file | Appears as encrypted/random data |
| Visibility of secret data | Hidden                      | Visible as ciphertext            |
| Main technique            | Data hiding                 | Cryptographic algorithms         |
| Can be combined?          | Yes                         | Yes                              |

For better security, steganography and encryption can be combined:

```text
Original Message
       ↓
Encryption
       ↓
Encrypted Message
       ↓
Steganography
       ↓
Stego Image
```

This provides two layers of protection:

1. The message is encrypted.
2. The encrypted data is hidden inside the image.

---

## 11. Image Quality

A good steganography implementation should maintain the visual quality of the image.

Two important concepts are:

### MSE – Mean Squared Error

MSE measures the average squared difference between the original image and the stego image.

Lower MSE generally indicates smaller pixel-level changes.

### PSNR – Peak Signal-to-Noise Ratio

PSNR is commonly used to evaluate the similarity between the original and stego images.

Higher PSNR generally indicates better visual similarity.

---

## 12. Steganalysis

**Steganalysis** is the process of detecting whether an image contains hidden information.

It attempts to identify statistical or visual abnormalities caused by data embedding.

Common approaches include:

* Visual analysis
* Histogram analysis
* Pixel analysis
* Statistical analysis
* LSB analysis
* Machine-learning-based detection

Steganography attempts to hide information, while steganalysis attempts to detect hidden information.

```text
Steganography
     ↓
Hide Information

Steganalysis
     ↓
Detect Hidden Information
```

---

## 13. Security Considerations

Basic LSB steganography should not be considered a complete security solution.

For improved security, the project can use:

* Strong encryption before embedding.
* Password-based access.
* Data integrity verification.
* Capacity checking.
* Supported image-format validation.
* Error handling.
* Randomized embedding positions.

A recommended architecture is:

```text
Message
   ↓
Password / Key
   ↓
Encryption
   ↓
Binary Data
   ↓
Image Steganography
   ↓
Stego Image
```

During extraction:

```text
Stego Image
   ↓
Extract Hidden Data
   ↓
Decryption
   ↓
Password / Key Verification
   ↓
Original Message
```

---

## 14. Applications

Image steganography can be studied and applied in areas such as:

* Secure information hiding
* Digital watermarking
* Copyright protection
* Covert communication research
* Cybersecurity education
* Digital forensics research
* Steganalysis research

---

## 15. Conclusion

Image steganography provides a practical way to understand how information can be hidden inside digital media.

The LSB technique demonstrates how small changes to pixel values can be used to store secret information while maintaining the visual appearance of an image.

Combining **encryption + steganography** provides a stronger approach because the information is both encrypted and concealed.

This project provides a foundation for further exploration of advanced steganography and steganalysis techniques.
