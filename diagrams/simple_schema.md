
```mermaid
erDiagram
    DEVICE {
        str name
        str manufacturer
        enum status
    }
    SITE {
        int id
        str name
        str address
    }
    COUNTRY {
        str name
    }
    TAG {
        str name
        str label
    }
    DEVICE }|--|| SITE : "IS PART OF"
    DEVICE }|--|{ TAG : "IS RELATED"

    PRODUCT {
        int id
        str name
        date created_at
        date updated_ad
    }
```