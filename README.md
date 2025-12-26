# True Lens
### **Deployed URL:** https://truelens.qzz.io
### **Presentation:** https://www.canva.com/design/DAG8itvpVYY/yfpPqVB5qEVKEtpHZRCFKg/edit?utm_content=DAG8itvpVYY&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton

##  Hardware-Based Media Authenticity 

True Lens is a **media verification system** designed to prove whether a media was **captured by a genuine physical device** and **not generated or altered by AI or editing tools**.

True Lens works by giving every real device a unique digital identity created by the manufacturer and publicly verifiable through the blockchain.


---

## Problem Statement

With the explosion of:

* AI-generated images and videos
* Deepfakes and synthetic media
* Easily editable or removable metadata

there is no reliable way to prove:

* *Which real device captured this media?*
* *Was this media altered after capture?*

Metadata alone is not trustworthy <br>
Hashes alone don’t prove device origin<br>
 AI content can visually mimic reality

---

## Core Concept (Authoritative Model)

True Lens follows a **manufacturer trust model**:

###  Manufacturer Responsibility

* At manufacturing time:

  * Each device generates a **unique asymmetric key pair**
  * The **private key is permanently stored inside the device**
  * The **public key is written once to the blockchain**
  * The public key is linked to the **device model number**

>  The private key **never leaves the device**.

---

## Media Capture & Proof Generation

When the device captures an image or video:

1. A **unique cryptographic hash** is generated for the media
2. The hash is **digitally signed using the device’s private key**
3. This creates a **Proof of Origin**
4. The proof is embedded into the media metadata 

```
Signature = Sign(MediaHash, DevicePrivateKey)
```

---

##  Verification Process (Public & Trustless)

Anyone can verify media authenticity by:

1. Uploading the media
2. Providing the **device model number**
3. Fetching the **public key from blockchain**
4. Recomputing the media hash
5. Verifying the digital signature

```
Verify(Signature, MediaHash, PublicKey)
```

###  If verification succeeds:

* Media was captured by a **real device**
* Media has **not been modified**

###  If verification fails:

* Media is edited, AI-generated, or spoofed

---

##  System Architecture

```
Manufacturer
   └── Generates Device Key Pair
        ├── Private Key → Stored inside device
        └── Public Key → Stored on Blockchain

Device Capture
   └── Media → Hash → Signature → Metadata

Verification
   └── Media + device model number  → Blockchain Public Key → Signature Check
```

---

## Cryptographic Guarantees

* **Authenticity** – Only the real device can sign
* **Integrity** – Any pixel change breaks verification
* **Non-repudiation** – Device cannot deny capture
* **Decentralization** – No central verification authority



---

##  Verification Outcomes

| Scenario           | Result                        |
| ------------------ | ----------------------------- |
| AI-generated media | ❌ No valid signature          |
| Edited image       | ❌ Hash mismatch               |
| Fake device        | ❌ No public key on blockchain |
| Metadata removed   | ❌ Verification fails          |
| Genuine capture    | ✅ Verified                    |

---

## Use Cases

* Journalism & news authenticity
* Court & legal digital evidence
* Government surveillance systems
* Anti-deepfake social platforms
* Scientific
