Todos
=====

Current status
--------------

The program is able to crawl through all mails, and remember which mails have
already been visited in the last run.

There is a stash that collects encrypted mails and writes them to files.


Recommended test bed
--------------------

The following can be done without root privileges, unless there is an explicit
``sudo``:

1. Create a subvolume ``/tmp/Mail``
2. Copy all Mails to this by ``cp -a ~/Mail/*(D) /tmp/Mail``
3. Make a read-only snapshot ``btrfs sub snap -r /tmp/Mail /tmp/Mail_safe``
4. Whenever necessary, do ``sudo btrfs sub del /tmp/Mail && btrfs sub snap /tmp/Mail_safe /tmp/Mail``.


Observations
------------

It is very difficult to decrypt mail files and getting new mail files.  I was
not successful with doing that with PGP-based encryption.  I did partially
succeed with S/MIME-encrypted emails.

It is not feasible to decrypt encrypted MIME parts in Python.  Instead, one
should call an external program for this.

With S/MIME emails, I was successful with something like::

    openssl smime -decrypt -in ~/Mail/KFA/35559 -recip ~/kfa/Zertifikate/t.bronger/bronger_cert.pem \
        -inkey ~/kfa/Zertifikate/t.bronger/bronger_key.pem -out /tmp/35559_decrypted

The result is not the full mail, however, but only the decrypted part.  It must
be re-inserted into the original mail.

.. note:: If the above command fails, check whether the key is the correct
          one.  Over the years, I had to use multiple S/MIME keys since they
          expire sometime.

In many cases, the base-64-decoded, decrypted part looks like a MIME attachment
but with binary garbage in many places.  This seems to be due to the sill
present S/MIME signature.  I think that this ugly code is really a valid MIME
part that can be inserted into the original email, as long as the content type
is preserved.


Possible further steps
----------------------

I think for the time being, I should focus on S/MIME.  PGP seems to be a dead
end in email encryption.  Besides, I did not succeed in decrypting them with
GnuPG.  This may be due to malformed mails, though.  A possible remedy may be
the script ``gpg_butler.py``, used by ``decrypt_directory.py``, both on my
private desktop.

One could detect S/MIME-encrypted mails, send the encrypted part though
OpenSSL, and insert the resulting MIME part into the original message.
