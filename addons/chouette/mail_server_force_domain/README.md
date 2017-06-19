Mail server force domain
========================

Modify Odoo email server to force sender address domain of emails 
to match the configuration value 'mail.catchall.domain'.

This addon may be necessary when the email sending service only accept emails comming
from a certain domain.

Behaviour
=========

The default bounce email address is

configuration value "mail.catchall.alias" or default "postmaster-odoo"  
@ configuration value "mail.catchall.domain"


    ```
    If the sender address of emails ("From:" field) does not match the expecetd domain
    Then
      If "Reply-To:" field is not set 
      Then
        "Reply-To:" field is set to the original "From:" field
        "From:" field is set to the default bounce email address
      Else if  "Reply-To" field was set and match the domain 
      Then
        the original "From:" field address is added to the Subject"
        the "From:" field is set to the same value as "Reply-To" which is deleted.
      Else
        the original "From:" field address is added to the "Subject:" field
        the "From" field is set to the default bounce email address
    End If
    ```
