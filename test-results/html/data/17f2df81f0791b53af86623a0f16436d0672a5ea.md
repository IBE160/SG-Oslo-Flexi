# Page snapshot

```yaml
- generic [active] [ref=e1]:
  - link "Skip to main content" [ref=e2]:
    - /url: "#main-content"
  - generic [ref=e4]:
    - generic [ref=e5]:
      - heading "Login" [level=2] [ref=e6]
      - generic [ref=e7]:
        - generic [ref=e8]:
          - generic [ref=e9]: Email
          - textbox "Email" [ref=e10]
        - generic [ref=e11]:
          - generic [ref=e12]: Password
          - textbox "Password" [ref=e13]
        - button "Login" [ref=e14]
    - paragraph [ref=e15]:
      - text: Don't have an account?
      - link "Register" [ref=e16]:
        - /url: /register
  - button "Open Next.js Dev Tools" [ref=e22] [cursor=pointer]:
    - img [ref=e23]
  - alert [ref=e28]
```