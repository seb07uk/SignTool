"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                         Digital Code Signature Lite - polsoft.ITS™                         ║
║                                                                              ║
║  Project Manager : Sebastian Januchowski                                     ║
║  Company         : polsoft.ITS™ Group                                        ║
║  E-mail          : polsoft.its@fastservice.com                               ║
║  GitHub          : https://github.com/seb07uk                                ║
║                                                                              ║
║  2026© Sebastian Januchowski & polsoft.ITS™. All rights reserved.            ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

__author__      = "Sebastian Januchowski"
__company__     = "polsoft.ITS™ Group"
__email__       = "polsoft.its@fastservice.com"
__github__      = "https://github.com/seb07uk"
__copyright__   = "2026© Sebastian Januchowski & polsoft.ITS™. All rights reserved."
__version__     = "1.0.0"

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import subprocess, threading, os, sys, shutil, json, base64, tempfile


# ─────────────────────────────────────────────────────────────────────────────
#  Embedded logo (polsoft.ITS™ — base64 PNG 56×56)
# ─────────────────────────────────────────────────────────────────────────────

LOGO_B64 = (
    "iVBORw0KGgoAAAANSUhEUgAAADgAAAA4CAYAAACohjseAAABCGlDQ1BJQ0MgUHJvZmlsZQAAeJxjYGA8"
    "wQAELAYMDLl5JUVB7k4KEZFRCuwPGBiBEAwSk4sLGHADoKpv1yBqL+viUYcLcKakFicD6Q9ArFIEtBxo"
    "pAiQLZIOYWuA2EkQtg2IXV5SUAJkB4DYRSFBzkB2CpCtkY7ETkJiJxcUgdT3ANk2uTmlyQh3M/Ck5oUG"
    "A2kOIJZhKGYIYnBncAL5H6IkfxEDg8VXBgbmCQixpJkMDNtbGRgkbiHEVBYwMPC3MDBsO48QQ4RJQWJR"
    "IliIBYiZ0tIYGD4tZ2DgjWRgEL7AwMAVDQsIHG5TALvNnSEfCNMZchhSgSKeDHkMyQx6QJYRgwGDIYMZ"
    "AKbWPz9HbOBQAAAmw0lEQVR4nKWad5xdVbn3f2vtfvo50/tkJskkM5NGQoIEMyGELiBg6CJcRTAKKCCK"
    "XJhEr/0qvoJSBY14pYggUqWENNJ7pmQm08/0Ob3tttZ6/wig6PW+9973+Wt/9mfttZ7vetZ+VvsR/HMj"
    "AMQ/vBCCgBABAO3t7bSzs4U8//wV7KNCofq6pvlLlpdWlp1WUVa8oLy4eFZpSbjUq+l+j1cnlFKYBYsX"
    "LDuVSGVmZuKJvql48lB0OLp7/4F9uzHTPf5hVW3t7fKWjRsYQD7mx//EyH/27rnnnqNXXHEFA1BUXNFY"
    "V1Nf60tOjCYHBnoGAGTWrVsnNTc3i40bN3IA0GqWNjbPnX1JQ0PDJS3zGpYsaW3yz5lVjbDfA8IZGOe2"
    "aTosmc1pjHFqqApTZEnSNRVUVZErWBgcncKx4/2xY919O3q6+5/f/f5bryEdjQPAunXPSR/rxL/zVwiB"
    "DRtANmyAIITgbwPznwECABadtvaKprlNT9iAf3Im1ev1G56wphozU+Of3fzGH18DgMrmtsVz5jbdtfSU"
    "1nUXnr1KnVNThkIu6x4fGLf29Y5ae3rG9cG4xRMFgazLFIcRRQBUoYLrEhFhQ3KrgyoW1BY5S2eXKwtm"
    "V6qRogjpGZ7E21t3Te07cOzJvQd3PJDrPzIlhCAbNmwgGzduFO3tgmzYcNJ3SZIY5/w/C5z4GKAQghBC"
    "xFXXf35hUWnVJ7e8++7y+acsuyR8ouPN03LH6kcSdGzw3M/Wj0eHj5SXlP7RptK8ytpZ31l38TlKWUA3"
    "3z9wLP27vxwydo4UpDg3NHhCkuwPQNN1KIoMWaKgFDjZwwSMCbiMwbFt2KYJYWZFwMlYp1Zq5hVnzMbp"
    "S5oCMxmbvvDqO5P7Dhz67vY/PfkLAP9AAgA//s536poWLa3Zf+SAOTESG3/00QdGP4T8awSFIALApZde"
    "P6dp0YI/7tqzJzV6tHfkmXldK5f+6jvVyUc2of3pxEt7l55N55SWXNTa2vTzT1+w5uZn//Su9cSWExiy"
    "QwYtrVID4SB0RYZMxEkgAIQAlFAQSiBJ9IP2AC44hCAQAmDpNESoGOl0BrnxIbeGx50vX9Bqnn/G4uCB"
    "41H6+pvvvrvrvc03XNccmzxn/S/m+iLBBV5vaBmR5BWgqHj00adefPPNt16sa5wzN5NObN38xkv9gPj7"
    "ISoIQNAw95Qz1YDv62oqn36xvvv8hosq/DgyIb6+p+rAy5Gm8aE9O62NG77Z9fv9sbsOJw3F29As+bw6"
    "FCIgUUDRFGiqAk2RIVECSZGgSjIk6SQkBCCEgMMYBJUQGxhEdmwCWnk5OJUB5iIxMoqk47JPzULsqfuu"
    "Hxkei8Gx8q6mG+F83pxDZYXk8gVYts3e37Ht/gce+MXahoaGkXzBfKy4KLJ2z9bXNq5bt06S/3HoQuRS"
    "yWPZXPpouLL6qg3jVcM3PzMTPJQPuAdK5zUFzcym2WdfPvnYcPGmaKBKrawPQBIMskzh8erweQ3oqgxV"
    "pjA0FYahAZzDZQyapkKWKAghYFzAdV0QWYEbHYbj9YBYJrjlQHAOvy4hUFHizKmxPXsOdDbnChZhjMF2"
    "WZZSckKWpHzA75WsQv61zdt3RZpbWhb6fIGSRDJ2huPakwDw/PPN4u8AIerq6vShof6pSNms7qCmGiPV"
    "p1n3Rgd206qaYiqJGtXO1zeuXHvljFyUETP5CCGUGB4PAn4DMoBsJoOycCkCPg9sy8LQiX7MzCSg+QIo"
    "r60CZwzFIS9qy4LgLgMUBYmID5lYHKrfi6zIwuP3ifT4BCkr8qVLvekjI5OxCkIEV2TJQ4lkZLL5ikQi"
    "qaxZfYbmNSpeO3Lw6NpZdbXJsgofJUTkuw9u2/RhTvkIsL29nW7cuJHPWbBs5aVX33TvG6//+Tg1grsv"
    "pzt52+eqLjhx4N3+R3oX7rJlvTYyujewtmX2y7+X5l41VSBGQJcRm5yGbdmIxxNoqClG0KfBIg76BqKg"
    "sgJ/sQpVlZDOOCCEIJXOIZO3EA540ThvFnwBDzImB5iNkppSUhz2IFBZ5uk8+sZMWMHagmUhm0lbyWQy"
    "l0wmk8NDw2Z0JFpYu7btoqBhPC5LtLFpbuNCsxB7efNr4/kNGzZQAPwjwI0bNwohBKmYNetERVUduKQs"
    "i/Ud33beLdF/mX3LdcaCHZMtb3z9yOsjbIX3/d0HrGhOFLItLSqXOLcEpYOTKQjBISsauoemcWJkBpGQ"
    "B5akQYDAAoVDJJggYJRiYCqDvtEENIWiuaEcZU1NGN++B3nLgpNJY9biFpHN275osLrq9Sd/+h/J+IwU"
    "CvpKZCrDta3xgm2aD//kR2N11VVF97R/64J8LqdEgr4Hv3D9t4Y+DNbHpom/eQ4CaPAVVX+uomruvMcv"
    "PxD45LL0adEBMnDDM8v7BlNy1503XdPhnb/0zn5SMkelAlSR+fREgjCXgRBwzrgglArGHFmWKEAkFgp6"
    "5UhRUBQsB0GPgoLpkHg6D0IIBIgoD+oY7h2Az6NxDS4qmuYimzOJK1FCk6MH8kd3Hn/wl7/ycZDKT5y+"
    "Irlvx47vfuX227zLTvvEJ7dt2eabnh76wYM/+lEUf7cC+yiC69ato88//zy7/tZ71t5847XXr7/plt0p"
    "M3vt3W8umbqsN/fLrlxVUdf44JWf/+w655ZbbxnoOrz/DvPdFxp3H+n+5NRMfLHX0BkIJUSSFYkS1eGQ"
    "vT5PSpVlIQQC1OdNJJiQVFWmaUXhiqq6uqIAABhzlJG8A9OxBSdETedyOPJKHhDCdSwLtiDVpaXFxffd"
    "+430t7//s8z4xHRVomDf3nvs6AtXX/mZ27Fqlb5z1+6XAUT/ZhX2MUDyXHOzCNUtCgX84W+XFBUXwmWl"
    "jdnBKAuUFu99WEoVVZfkJhc1zX3RcvnSeNfWzy+4beePUNNwWm3tQuoG0mVjkxlL9hlEloRmWbZaXx6Q"
    "PKGgPDKVEjJ3QpFQOako9suDEwnJZoR5VI8NwQmVVVGwMrqickRKA/xQ16ChuAyqSkR2LOYgmyHwGgLv"
    "bcpWVZSF5i1sLuvv7n7HCTcseOxw/k7fg08c+fF37l46MTHx+J13/ri5o6Oj8GGC+Qiwrb1dIhs3uhd9"
    "7s6vntI6F3fc9c2xWCxZYxd450RrR+tj93/jlD9te9na9I3t316hn9Go6VKAllc36GU1s5O2iwWL56PU"
    "dLwD4wmAUtQXe1FTHsH2w4kI06ug6wR5xS5LER+WL5+N6HQGE7E8dFWCzTg0xY851cUYGZ3GF85sRWuI"
    "gjgOEtkC3jo8gd1jgqnlleNUcK3naIccm4qt4l5eVbzkHPz81X2pL15zfGR128r6sdHRr9y5/us/XL16"
    "tQzABQDa3t5Ov9zSIgB4qqsrb25qafXtOdKx61hH58GRgV4zk83MfnPkTSS0mJa1EqfksnkMTcY07rIC"
    "M3OCOZZ78HCv8EiuaCjWRFC2RUVQx/7dR/Gd5U9i840/ENc1bkY6ZorR6LjYfbBHFOlC1EdkkUzEhJVJ"
    "iLmlhujs6heR/IT4hC8jrOkxkRqLCp8VE1cv8oqgk+ROLse4pPrI0otNfe315aFzrhOSz89IXWvwvp8/"
    "bZcHDbekrPzOa6+9NrB69Wr2YU6RP8w2az7zxS+tWLa4fEtfDG3X3HzevZcs+cXW94/McgKZI72HDyzM"
    "9CvjwXh1cd7ORjQYTnWDQS3qJal0iuheg+w5OoJlrTVYPDeAN7aMi++3/Ubc0LrLevz1hYWfX/mUfzoF"
    "5eWBU0F4AbuORtFUV4Q5VRHoioL+4RlEhyYRtWzo+TQunB+AoslIFkw88GovEpZBVCrAFYNIJZFK++he"
    "YQ4NE9nro0UtK/DnY++Xd3V2Tiw7ZVF1d1fPpwkhm9o3b5Y3nnmmSx/btGnWxMTEWRvv/nLdyqWtj57b"
    "XPa9r11y+ntZU8xde/aqNzFjpGo7lh2+JHBD9M7bb0s3tzQP1VYEzPjwGKmtDKO0yItsOoeKYh80WcKO"
    "gwOwE2nnsrlvpx55ezb95s9uDW47zHBWzVZhpQUId2HnTZwYnEDAZ6C7bwy9+3tx4VwDC8oo3tkexZNb"
    "htEznsSmLUOIpgmIKkMIEEooCIiAZUPx+OGb3Upkrxesosn/qxfeciuKgwiGQzcCAFav5gAgP/74prmP"
    "P/70dclEisbisZDfHzqjqrYuGAqHSxa2tPxyy7bN1aMTE5F8JlsxEx3tefjxR97Wy2ZJ+cRecaxjAK3z"
    "KhAJ+qFqMg4e64ft2pBkVXrt/TJr/Zk7wj75J/hkzWHp4WdXWqCOls3mEfR7UFs/Gzt2dqLJb+IHtyzA"
    "VW1zMDiewHsHh/HNZw7j5aMJjGYpiCGBMwZBSA6CwU0liG0xATMHPjiAkDcgwvXzyCuH3vJ9eWq8UFpa"
    "fPo5V36pZiMhI+3t7ZTu3dvZ2T8wvC5XKFzjMTznGR6j0us1mFfXRoIBXzoUDKIoFHbCobAs6R5D17Ws"
    "FYtLkAhc18X+Qyfg9WkAOPL5AkxTFYwEpI2bL9O1eCJ/25qX0NkTzr54oo0oNIGgV0WoZB6WiN/iJ0vu"
    "5eXMwrVrZuPbD7+MYz0DuOasufASF6MZQNZkgHOAUEGElCNUgq9xHrSKWqg+H8ILl0L1B0iotAijSon3"
    "WNeJRGNDvVpdVXrWB7MDpUtbZpFIyP90OBR6OhgO/z4cCmw3NHUclFJBqSKEEI5tG67rggs2FQoGUpPT"
    "MzIEB7MclEQCyGWzSCYdhMI1WBDuIjee9mc4RmPw3j+0OdYYnPveuYo6JKDKAIhnjjhP/ym+3/SN3HPv"
    "tBQ2XPcJbN3bjW9/73Xc8N0/wnVcfPPS+YBZgPib3RwHJ1SmCNbUIVxZAo26qFi0EL5QGB7KEW6cr+3t"
    "HrbCPg80VWs7+dVqyMlkQs3Y4gIqmxWcM2RzebiQ4A84cBxGZElOc8bmCSEgOE8xDhYuDTKYbqGkKID6"
    "mjAOHYgiQkfwzOeexin+/WbvIEN29oPqZy542PvAq/9q33X914y+X+9AMsdwa8295Mv1v3XOfOR27B1s"
    "8Xqf+BOe3ngtbvnKWiyZV4FMzsT/efkQ9EgAZiYLEAIqCQjmgFKKcNBAjLog4SDMyXGU1FRBWAXBRRE9"
    "OtQpXWbmoWn6EgDYsGE1k9NuLkthDEjAmKqpaa+uy5FI0JSoGrIL+STjTKVUmhFCVEMQnYMjFoshPKtS"
    "VFSEcfj9HlTrwzjwpe+7bx7wxE7Zer/HCS/Ux6amSVXFlLxk+Xfk597aw77f8nWrbWFMmh4S1soHvoDB"
    "qosDVafmcGJqCM+/9C779k1tJDoRF3/Zeggpk0jFVSWQWQRjQ6OwbRtEEEiyhIAuQeIWrHwBQZKHrEgw"
    "Cy78fh+GEjk9l8tYuq43BmsXhAkhCVljLGVyV+YQlXBJNQH1zUzFpLnzqydlBTRfKEQEhC2EADiPzaqf"
    "Ne0445QzS+o+2gs3nxUvX/Mg+/3mmtz6t/41hAa/Nr+hHMWz6/CztzsB1gdIMjlQ+VXc+XKP05Nu0hCp"
    "0qSxHoTqa1GomIsbfvgmPXvLCTKWYejoTwOREki5AZSWl2BOcwPiyQKmOkGoLMOjcKjEhqxrUJwMWpoq"
    "kZmSkOcKBo4GeS6bzfl83khZSaQsNYwEjUajpu26iu06fsexYTnmtMPs7PRMPDk4MmBKVMpwxgnnAnCt"
    "gcq6mrTq8yE1FHXttITL57wPvZA01793qyHPUjSJZUXXkRNIpTJYsbIV4fIKnLJiMZ0IrvG4S9f7tOoq"
    "DciCSzKGuk8gG09h0RWfIW+NqegYJ5Aqq0FlCYxzjA+OoPdINwxdJb6ArlmWi/G+IaQm4hCltRjrPoHx"
    "iRjiiSwiAQNFtdXT2Vw+49F1MKJFAEAuKiryOUKMgEMnBJKTd92pofjhfM5eQ5laqcpymnMWEYID4BKz"
    "GIjjECgShyvExZX7+Kajy0DUsErsPBjViKTKGOwbRSaVxsJFjeg51ofxgSgqa8vQ2joLvR0nkI6nIOkq"
    "JoZHYWayOGXFYoz2j2ByZAxEU0EBCE2F7Tjo7+wVWiZvm6aNXfsPI+AvQyGVR3xkFDPvHkU+lcDVl3gA"
    "M1s3E7NTkqTDdZ0QAFBZlrkgaCGUzGeumKtX4tC/vnu+W9UQ/HM6lS1h3KW27YSZ6+YgaNdULKHWNlRY"
    "ILoN4pBabzLTmaplghLBGBGCE8FcARAJmsfHentGMT4yA3j8GBuOobNzCJVzGhAqjnBWcASoguRUAgfe"
    "PwRvSREq5zY6wuacuwLC5QAoIGtwXBfMdQl1LGQzBUBWwfNZuKkEmO2Auw78Pk+cMZ5hXAAcOgDIk5OT"
    "+UBJrQnBBefCNUpJXK/LLND9fGd+UvgVTcm4ruvjnI9AJnoul2GP/ceequDke3+RfeWdv9ldZo3E8nqV"
    "s0NTXMiyqglV05msqqjXC/mx4UmlLiITVZUhF1MwnuUR16IXtFXY0T5TEYLrsuwXtuVwIQZE05mtyW7v"
    "uDcRy2gOYyJXyMgQipMvNWqopC1089Mil07AU1QD7tgwEzEQw49X/3IE2aN7vGdctThTKJgoFAp/3U0I"
    "AS4EiKQSZeqAfdmt5a8+XVQavrFxVu0LBLLLBWeCM4BDnZme0oXsyaWOvvQ4AN+TO9EG0r1eMZQzqKzo"
    "iqJAllUuSTImthA5EAzKqqpBcAdz5p86oaoyTQ4OlQ73F0NTZRBKbUop4ZbJXcax9zdvU8uyeC5fQMGy"
    "kUmlieO6wrZN5tXVFKcIUUUVIh0HFBUimwEML5KZAqyCm+LcRSHPYJvmyaVac3OzEp3K5IUQAAOTZKky"
    "Ulp0t6Jo4IJbgnEZQmQ4c1VZU2zO+HFV0y96+Ld/bMhk857SiN+amJ58qbujayiTzMwTBJrLmN/QlDQk"
    "KbV92/tvp3J5SZZkX1fvsYwqy66uyNxBUlTXVK2qr65aAgibCEEs2yKO7Yh0Jh2wbYdKMk0zl8kQ3CmL"
    "BBiCpVVW9phQisogmAORz4JQAaqogkIitqqO6KruT6bGkEnF8gAgy3JMAVQhhBCEAEJwzlzXolTWXM4A"
    "CgEhBBfIaV5f2boLz9z33Z8/lZWIqPnL22+fy4m+QChak6J5NEWLWIyLgOzVkSWALMupyro5O+Hm3ti7"
    "5fV9AOAtayitrq67kgvkvdXNHfLseednLMtHFQNccFBKERQnT7+5EBW264K5jI0VXOnX20Zhu4Adj4OW"
    "VoB7i4WbyhC1UhVgHBIRY4qqtiSTCZsVshMEgHzkyGTOW1RDCREEQnAuiMIZNwTjsEzLAwgIgDPGHO7y"
    "aFtbm3zvbTd2A+iuWXrOLaoR7MllxnbaXKxUDe9S4TpR07J/noond2K8c2r2ksVPU4EJAPsAIDfZX5kJ"
    "Rm6jVHYeu/+ObwGBa6WlawpNLfNb62orzzX8Qc2rK16ZUlkSQjZ0JSgLt4RK3Lm0OZzPVszTHUJ9puKT"
    "c8WcJBJJOGoOWUYhR+QRIaTlM9PTWTiJBADIS5cuVXoGpn4BQo9KRPZSRZJkRSGSqkhewzjouqxecEJk"
    "RWmxHeeCLVu2/HL52qsuVD2a33LcItXwhZWK0jEqrM05ixuRgPfNtatW7lN0XTcMb0MkUnQvkSFTiIt1"
    "RaGhcMCRhLhdlWSxdcfWU/2GN1NfXzE6Nj6JlEWCHp8vw83sTFlxqCwcDLoUbsfYYF90+dLFbmVdLek+"
    "3kd1w0NGxqcXjSYiDb5gqCiWTEv9o9NOoaKuczKRvH1qcroDwAwIIDc0NPCOvrFqieFaQoUkHMY44xyc"
    "67btjAWDksrBRzLp1OOOaT+7ePXl33Kd/OdJOndElaUBDc5OzaOXyFSZVVrsPaTpesOxIwfvVhXJoxse"
    "W5EkTdNUWdM0KeD3smAwpFEK13bdYEtTU960Le/oVMJOpQs8k8mymfFR3WaoyeUK/UsWRRIPP/pUOpHO"
    "rdx+6Li19swz5d6BkfmZVKrjU2efMd7XN1g9PhLNLV95htcxzQNTaeqksqYxPjnWBcC8//52SmbPnq1N"
    "Z5wKXfV4C6kZyzD8eqCoSM4monG/359fvnxlVQ7O+OJT17Zs37Jj7dT0xJlekeuyLDOuSHJQkiTiNTwT"
    "oAjIsiJ5PJ4sZCKpVNG8Xg84F15F03MSJSEOVoiEIx6vP1QpqHLK6PDQVkKhWKYVcxxHcoWgyWSypK5x"
    "XlDVjclbrl83/InV508zzu4pKSkVgUCw+xOfWB7KFnhNz/GOvnvuWh8rL688xROMyGPjo/ft3rZDGZ2M"
    "37/pqSdvy8cHHyJok0hbe7u8GuA/ePSZL5bUNl0Q3dNxB9AXO/+ar37Vtk1PIBAo9wd8Z2RTSfdYR+ds"
    "VaYHiBAZQqhMKE0Zhm4oumZ6dA90TXN8Pp/w+/1UolQJh4PMYxiWxzCYLFNq2bZm6LrNXCeUTGfLnUL2"
    "fcZ5xDIL8XQmXWqadpEQTJJk2WdzRb7mik87iqIcPXfVmW9B1dYSXW+sra7p0b2+M/r7+t96/ZXnaVVV"
    "9U2jo+PpF19+9VTXsf+wc+eeuiPvv7ZMCHFi9erV0kcbrvu+97P1ybz7i8qyovdvvfHKR5989tXfaLoO"
    "WaKQZcrHhgfO/dmjvzM0jaqOA9fn8yfC4ZCUY5aQHYmYdqaCM6eCcF4uUUlXVVUoEiGSRFWJyoIqRNIk"
    "hYBSwQVMQLhmIZs2dMNvmbm0aVkeiSicUkBSJJJK5+0N992ZXL3qzH8H8K7PUN91bWcsnorTYNAnAt4A"
    "Ridi9xJJmcW4vSeXyryw6+DRH0aHB/dec+Wn72qsq9sGAOSFF16vCBSHHo2OjrcOD0e57TjFhFJFkWiS"
    "ygoEF5AVWT5yrHt/V8/Aa5JEOBdCCECanknysrIyWloaFuAs4NpOqeM4RYRzryRRUIkS13HDsiLbtm0H"
    "k+m0pimqXVlZEWdMQNU1mxBwWVYpEYLb+TwVkiTMQo6kkmm+bOmSUFNjXYvDhV/zeDTXsi3OHJdQCZIs"
    "exyX5WzbdiRJopy5HgGekiSZhYI+WlVRsSs+Mf0l8sdX3379uRdeXvXsCy8TXdcNQQgIpVBVFVwAmqqC"
    "ECAYDINSBYpy8qy4OBLEFZecgwPHjqPrxDAMwwNVUaFpJ8twISBRCl1VwJiAx1Bx8bltYELg9398Az6f"
    "FwIEnAlwziAbOsrnzs6OdPb4tEhYeEOBXCqRIgWX25mZGXn40EGtZtFCBMurFTOfwejRY64Obuq66g4N"
    "jyqmaQrmOp5cLkfzhax1+UXniWvXXfqWPDY+2frn194qlJQUF0mECMiSrSqqbZkWLSsrtuKJtCHJspFO"
    "JfMVZWWmEK7oGxzxnXHqp2Lr/+Xq8MYfPZT502vveJctXmAXsklleqrgdVzHKS0uMimlZDCZ9diW6Tz6"
    "k/uceXNmKRt++BA7deFscfG5q+kNt7YT3ePRzGwW9SvPcMqu/LTe/e2fiPLTV2WCTU1qMYNseOH2v7uN"
    "Vi1o5fMu+7QydqzXLZ9TS7Y8+FDu7MrQVOui5pzf5yHhSIh+6Wv31xw82hkuKoror731XuaUxQtXyolk"
    "ChIlkuAM06m0+NYd68dvvfnG8OTUVLKlaY7/hVffTNx658bMpkd+5J616nTZth35rvt/kNQ0BYxzbWAo"
    "OvHYv9/HVp52ipzLF9wbvnxv/rrPXibfcNWn4biu/Phvn4vJsuwuP2VhaTKd5q3z5iY/c8k5RQG/X7pz"
    "/bXpDT95QoZpKrbmd0fjUMaio9ahr3yBf3LDz5xA0yL17euvtbMz0/TKp1+Ro5N58c737ivMDI8oqbzl"
    "DZ232ugZGebz5zYmG+vq7OlYvNp2bAjBIVFCLMvmlDHOOXdEJpt23VSC1ddVKcVF4cBDj/46/cbmbfbl"
    "F53vferhHwycu2ZVxdqLrrYOH+2Ufvpv90inLV00JlFKJYrspZ86pzyZzPC77vnuTGvTLPemz67zr79r"
    "o/Xsi6+Zt3/xc/7oyNg05xxbtu+J/fa5F23OuXW8byD7y1/93o0nkko8Ni1ymk+aScOdGhm2k+mML6NF"
    "MDWddWPjo8H4TMy/7ZEHaA6qtOqhZ/ynf+1+ahiq9Mpb75b8/oVXam67e+Pii67+/Km9fX1+xzLddCLh"
    "CuYwVdOSVJG1uKqqzLZdGa7jFoXDFoD8I0/+tpMIISanpnlNZWVxdHSisOWNP03kCyaPxZPC7/MK07Sc"
    "97Zul6/67Bf3BgN+85cP/FvFZ6+4eNB1GXniiV/nY/GExTjUruO9nFLqvPjKW3hvy86Apqrurj0Hk+/8"
    "+Q1/fVXpNIRjTTK/MjjuspnRYdkWwhwXEXJiYAKpqUkCQ0fHa3/Iv3TJqX1Ht++cwtnnaoGmlsnkWFRP"
    "JBNeCFdnrm3kc1nFsizZtUxZ1RSXEszIlm1aDbPqf7pvz/4EYJtNsxs/F0+k63oPbltTVlZWtO/QkW9m"
    "kmnjrDWr2w8ePlTT2NgQ/tWTm37X0jx/xcjIuHLP19b31lZXtyWSKcIYI8/94SW3tblZfu/NP1QvWtCs"
    "/ea3z/bksxkfACM6FuW6SmgylcWatpW1N950zb6ffK994d333Df9MvxVhXhczcUmJa2onM8oQWqO74UV"
    "H0Px2Zemqm75t0Ci87AyHpzjiR2IJscO7AYI6SSu9SDnoPhAYkIoiGAuWubPL81ksp+ULcvO3nTTTbv2"
    "b311s+HxlNu2+/2JiUkxNjF++xt/2Zq5df0N7wAoHDnSuXfB/Ka6jq7jx7522827+/qGTmVwjQMHDue+"
    "cMM1zyWTGeOMsy5QOw5szy9c0PrAtVddVt3d3Tv5+RuuOrDotLMXAug/dOjwZebMaGbrjh2dV17+6chn"
    "PnXW4Vw2Xbxr94H67Ilca6GoeJhlMovzstYbf+2hVKHrkAVJ/czEljd25z3FIc9p55q+sOfI4K0X63a0"
    "P69V1+21o50n/vYWl0oUnHGsOXPNDZMTEwvJ+rvub/f7git+uOHOCwCgq7vvUcd1Cwtbm76Kj1sjIDWU"
    "zVmsts6b1+A6LFEoZEJFRcVaLB7Laqqq1NXX0aY5c3OpVKYwOjllEU7oiuWL9Fwuh+O9vSFwEvb4fVnm"
    "2k46nXM8hu5JZnIFr6FF/MJmHo+RK66fnU3G4sbUieO6SYibtEWY2YXM+InjvtzEaMLKZXqiVv4QgEn8"
    "Uyvxffnu2w9mUqn7SVtbW6hlWduWUKSkIxz0PxIuLx5yHIlcuOYTsqJqbPvO3SHDLw1ee8Xnf6b7gtdT"
    "wgEQqIoKzk5qXVRVBSEUHkMXpmURQijKS4pw/rltid8990pYkiQoiorS4hDXNY0Nj00pLmMoiQQR8Hl4"
    "RXlppn94VBocHvVx5p68gKYQggtCcFIw9KEyyjRz8Hq9jd+86/bg0kUtuTlz51uHDx41ZtLTUs4W0vTE"
    "VM3oSLR9YmJ84pknHriEAEDD0qXBlaee+W9ew1gcDgVNKlFzOpZolFSdLlnQ/O682XUPrT37/Fn+SNkr"
    "RAgLlMiyJLl3rP/CCcProZJE8oqm0/LiIs+xzm7U19VQidLEggXNkef++EqhqqJcZ4ylq6srgrlsXtuy"
    "Y1fs4gvP0XLZnFIUDikd3T0zluMqjfU1vo6uHqeutgb1dVX0q3d/u3hgaDioKLJwXeYKgDpm/s/PPvXs"
    "9SPTfff0DkbXJuPx4qJIsIu5TLZtx5vJ5uREMvbKC5se+Z4QgsgASP/+/an+/ftv/XiY/Xfp5TU/+p0v"
    "0pE+0T8JTHayQPC4qnqaKCVIJJLukiWt8tozV6UmJiaURDKVGRgaDV1+8XmxiemY8cOfPhx65Q8XmbVV"
    "laAyjbctP03bf/BINlcwC5+//qpcdUWZvH3XXrerp8+srKjAimULskc6juvXX31Z7FhXj64qihQJB1nX"
    "cZNIkocCQoIAKGE/PvfcxVZ4/irOCrll6amxA8iPXwcg9TH3CQEh5KPbDdLe3i5t2LCBAcDzzz9Pr7rq"
    "SuYtqrtLC5b+2BMIT8iydEc62tNtMv5DIqSVXHDP8qULs5IkZwghbGAoWnTxp87Jb9+xl+uGJqanp9XG"
    "WXXTsqyQcChkJZKpyqnpaal5/pyEY7uK5dj28FDUM3/eXDM6OmYlE6nwJ1eusLZs38Uj4VBSVxXpcOfx"
    "eZl8gdqOkxYuG1ao+EW4pn4fiPpLq2CempoaOVDqVS4dHOweZoxRSiXOOaOrN2ygWzZuZPiYGO8fTQLA"
    "lEDZVUaw5PFIWY2PUmn3gjk1m2oqirKvvfFmpv/Y3mlAisBTUWToNF2ID7vQS70AoHu9xExnKRg/mcAp"
    "OAwDyCU+kHlIgO4hMJMC1AsQkgSbMaEWa9ADQeQyNth0N+BRv3jrbSWhSCjw6js722zH/UomFUdmZvIP"
    "KsMXEon+FPDXaeLv7b8C/AjSX1TZRFTfb7zh8hUlpaU4b83K6RXLFg0tXbLwEZmZL1XXnnUtSqsvkYKh"
    "RkKJAUkyuYANSlwQCSD0ZFNC4IOsAXAXgjNQSmQIrhDBPRBEcfLZGOKxV5Ui5dexri2+w51dd+w/2HH6"
    "629tLR0YHkV8aiRvZZLtmenBf//Ax38K998BBE6enboAdH9Zw62S6vm6N1BUsnhRK85bswqtzY1joZDv"
    "5Wf+tO3Eg8+9V5FPFJZC97RA95ZA94DKCqgkATgpm/xAagghOLhjA2YOyGdTMAsd0Oi+C0+fO3b/7Vcb"
    "oVDg7K6egdM379iL97bswtTkOMx86l1WyH4jHRvZ9ze+/5dy5/8OIPA3vRQsq6uXJM83haxe5w+GvYta"
    "W7C67TQsXTgv2zSr5oii0IP7OkfGn3l1u7a1c4L2T6TDsB0NnPhApQ+qcy1iGGPVIS172vwy+9LVi8ia"
    "Fa3FAb+3ZWR8asmx44MVW9/fi2079mB8bBSOld/NHOuBxFjPsx9UIAH4ZxLn/xXgB2XbJGCLCwBFlfVN"
    "HMbNkKTLVcNXW1VZiYULW7FscSvmz64VTY01M1XlJdOgygzAklNT05mxyQnqM7zgLvOouu61XVbpOLw0"
    "nsoER8amlGPdvTh0+Bh6evuQSSXSjDlbwaxfxaI9f8JfI/VfDsn/H8APjQLrCPA8A4BgsC6k+NTTOVUu"
    "FIKsUDWjNhAKhUpKSpTqygpUVZQjEPCDcQHGXQjGYTsM6UwGiWQSMzMzmJmJIZVKpWzTjHLudAvGNlOS"
    "eWN6ZKTvr82ukz5s839i/xvAvwFtox9GFACWAspI1az5rtCWMGAJgCJC6CxJkryESn5ZkjgXnAHIcJfl"
    "GGNpLpxhIkSvArLfzk92plKpxF+baKdAJwGe5/h//Gv/zP4vXMz866K7pVwAAAAASUVORK5CYII="
)

def _get_logo_image(size=56):
    """Decode embedded logo and return a tk.PhotoImage (requires Pillow)."""
    try:
        import base64 as _b64
        from io import BytesIO
        from PIL import Image, ImageTk
        raw = _b64.b64decode(LOGO_B64)
        img = Image.open(BytesIO(raw)).convert("RGBA")
        img = img.resize((size, size), Image.LANCZOS)
        return ImageTk.PhotoImage(img)
    except Exception:
        return None


# ─────────────────────────────────────────────────────────────────────────────
#  i18n
# ─────────────────────────────────────────────────────────────────────────────

TRANSLATIONS = {
    "en": {
        "app_subtitle":       "polsoft.ITS™ Digital Signature Manager",
        "st_found":           "signtool detected: {name}",
        "st_missing":         "signtool.exe not found",
        "sec_file":           "File to Sign",
        "sec_cert":           "Certificate",
        "sec_advanced":       "Advanced Options",
        "lbl_file":           "File path",
        "lbl_cert":           "Certificate (.pfx)",
        "lbl_password":       "Password",
        "lbl_show_pass":      "Show",
        "lbl_timestamp":      "Timestamp URL",
        "lbl_algorithm":      "Algorithm",
        "btn_sign":           "Sign File",
        "btn_signing":        "Signing…",
        "btn_verify":         "Verify Signature",
        "btn_verifying":      "Verifying…",
        "btn_cancel":         "Cancel",
        "btn_clear_history":  "Clear history",
        "btn_lang":           "🌐 PL",
        "browse_file_title":  "Select file to sign",
        "browse_cert_title":  "Select PFX certificate",
        "browse_ft_binary":   "Executable / Library",
        "browse_ft_cert":     "PFX / P12 Certificate",
        "browse_ft_all":      "All files",
        "err_no_signtool":    "signtool.exe not found.\n\nPlace signtool.exe in the application directory or install Windows SDK (10/11).",
        "err_no_file":        "• No file selected for signing.",
        "err_file_missing":   "• File not found:\n  {path}",
        "err_no_cert":        "• No certificate (.pfx) selected.",
        "err_cert_missing":   "• Certificate not found:\n  {path}",
        "err_title":          "Validation Error",
        "warn_no_pass_title": "Empty Password",
        "warn_no_pass_msg":   "Certificate password is empty. Continue?",
        "sign_ok":            "File signed successfully.",
        "sign_fail":          "Signing failed (code: {code}).\n\n{detail}",
        "sign_not_found":     "Cannot launch signtool:\n{path}",
        "verify_ok":          "Signature is valid.\n\n{detail}",
        "verify_fail":        "Signature verification failed (code: {code}).\n\n{detail}",
        "verify_not_found":   "Cannot launch signtool:\n{path}",
        "verify_no_file":     "Please select a file to verify first.",
        "title_success":      "Success",
        "title_error":        "Error",
        "clear_title":        "Clear History",
        "clear_confirm":      "Delete all saved certificates and passwords?",
        "clear_done_title":   "Done",
        "clear_done_msg":     "History cleared.",
        "quit_title":         "Close",
        "quit_confirm":       "Close the application?",
    },
    "pl": {
        "app_subtitle":       "polsoft.ITS™ Menedżer podpisów cyfrowych",
        "st_found":           "signtool wykryty: {name}",
        "st_missing":         "signtool.exe nie znaleziony",
        "sec_file":           "Plik do podpisania",
        "sec_cert":           "Certyfikat",
        "sec_advanced":       "Opcje zaawansowane",
        "lbl_file":           "Ścieżka pliku",
        "lbl_cert":           "Certyfikat (.pfx)",
        "lbl_password":       "Hasło",
        "lbl_show_pass":      "Pokaż",
        "lbl_timestamp":      "Timestamp URL",
        "lbl_algorithm":      "Algorytm",
        "btn_sign":           "Podpisz plik",
        "btn_signing":        "Podpisywanie…",
        "btn_verify":         "Sprawdź podpis",
        "btn_verifying":      "Weryfikacja…",
        "btn_cancel":         "Anuluj",
        "btn_clear_history":  "Wyczyść historię",
        "btn_lang":           "🌐 EN",
        "browse_file_title":  "Wybierz plik do podpisania",
        "browse_cert_title":  "Wybierz certyfikat PFX",
        "browse_ft_binary":   "Pliki exe/dll/msi/cab/appx",
        "browse_ft_cert":     "Certyfikat PFX/P12",
        "browse_ft_all":      "Wszystkie pliki",
        "err_no_signtool":    "Nie znaleziono signtool.exe.\n\nUmieść signtool.exe w katalogu aplikacji lub zainstaluj Windows SDK (10/11).",
        "err_no_file":        "• Nie wybrano pliku do podpisania.",
        "err_file_missing":   "• Plik nie istnieje:\n  {path}",
        "err_no_cert":        "• Nie wybrano certyfikatu (.pfx).",
        "err_cert_missing":   "• Certyfikat nie istnieje:\n  {path}",
        "err_title":          "Błąd walidacji",
        "warn_no_pass_title": "Brak hasła",
        "warn_no_pass_msg":   "Hasło certyfikatu jest puste. Kontynuować?",
        "sign_ok":            "Plik został podpisany pomyślnie.",
        "sign_fail":          "Podpisywanie nie powiodło się (kod: {code}).\n\n{detail}",
        "sign_not_found":     "Nie można uruchomić signtool:\n{path}",
        "verify_ok":          "Podpis jest prawidłowy.\n\n{detail}",
        "verify_fail":        "Weryfikacja podpisu nie powiodła się (kod: {code}).\n\n{detail}",
        "verify_not_found":   "Nie można uruchomić signtool:\n{path}",
        "verify_no_file":     "Najpierw wybierz plik do weryfikacji.",
        "title_success":      "Sukces",
        "title_error":        "Błąd",
        "clear_title":        "Wyczyść historię",
        "clear_confirm":      "Usunąć wszystkie zapamiętane certyfikaty i hasła?",
        "clear_done_title":   "Gotowe",
        "clear_done_msg":     "Historia została wyczyszczona.",
        "quit_title":         "Zamknij",
        "quit_confirm":       "Zamknąć aplikację?",
    },
}


# ─────────────────────────────────────────────────────────────────────────────
#  Paths / history  (portable — no files written, registry only)
# ─────────────────────────────────────────────────────────────────────────────

# Registry key for persistent history (no JSON files created)
REG_KEY  = r"Software\polsoft.ITS\DCSLite"
REG_VAL  = "History"

MAX_HISTORY = 10


def _meipass_dir():
    """Return PyInstaller bundle dir, or None when running from source."""
    return getattr(sys, "_MEIPASS", None)


def _get_signtool_working_path():
    """
    When running from a PyInstaller bundle, signtool.exe sits inside
    %TEMP%\\_MEIxxxxxx which Windows SRP / Defender may block from executing.
    We copy it once to %LOCALAPPDATA%\\polsoft.ITS\\DCSLite\\ which is always
    allowed. Returns the writable path, or None if not bundled.
    """
    mei = getattr(sys, "_MEIPASS", None)
    if not mei:
        return None
    src = os.path.join(mei, "signtool.exe")
    if not os.path.isfile(src):
        return None
    dst_dir = os.path.join(
        os.environ.get("LOCALAPPDATA", os.path.expanduser("~")),
        "polsoft.ITS", "DCSLite"
    )
    os.makedirs(dst_dir, exist_ok=True)
    dst = os.path.join(dst_dir, "signtool.exe")
    try:
        # copy only if missing or different size (avoid repeated writes)
        if not os.path.isfile(dst) or os.path.getsize(dst) != os.path.getsize(src):
            shutil.copy2(src, dst)
        return dst
    except Exception:
        return src  # fall back to MEIPASS path


def find_signtool():
    """Locate signtool.exe. Bundled copy has highest priority."""
    # 1. Copied to LocalAppData (bypasses TEMP execution block)
    local = _get_signtool_working_path()
    if local and os.path.isfile(local):
        return local
    # 2. Windows SDK installations
    for p in [
        r"C:\Program Files (x86)\Windows Kits\10\bin\x64\signtool.exe",
        r"C:\Program Files (x86)\Windows Kits\10\bin\x86\signtool.exe",
        r"C:\Program Files\Windows Kits\10\bin\x64\signtool.exe",
        r"C:\Program Files\Windows Kits\11\bin\x64\signtool.exe",
    ]:
        if os.path.isfile(p):
            return p
    app_dir = os.path.dirname(os.path.abspath(__file__))
    cwd = os.getcwd()
    for p in [os.path.join(app_dir, "signtool.exe"), os.path.join(cwd, "signtool.exe")]:
        if os.path.isfile(p):
            return p
    # 4. PATH
    if shutil.which("signtool.exe"):
        return "signtool.exe"
    return ""


def load_history():
    """Load history from Windows registry — no file created."""
    try:
        import winreg
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_KEY) as k:
            raw, _ = winreg.QueryValueEx(k, REG_VAL)
            return json.loads(raw)
    except Exception:
        pass
    return {"certs": [], "passwords": [], "files": []}


def save_history(h):
    """Persist history to Windows registry — no file created."""
    try:
        import winreg
        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, REG_KEY) as k:
            winreg.SetValueEx(k, REG_VAL, 0, winreg.REG_SZ, json.dumps(h))
    except Exception:
        pass


def push_history(lst, value):
    v = value.strip()
    if not v: return lst
    lst = [x for x in lst if x != v]
    lst.insert(0, v)
    return lst[:MAX_HISTORY]


# ─────────────────────────────────────────────────────────────────────────────
#  Design tokens  —  "Slate Dark" theme
# ─────────────────────────────────────────────────────────────────────────────

C = {
    # surfaces
    "bg":          "#1a1d23",
    "surface":     "#22262e",
    "surface2":    "#2a2f39",
    "surface3":    "#313847",
    # borders
    "border":      "#363c4a",
    "border_hi":   "#3b82f6",
    "border_md":   "#454e5e",
    # accent
    "blue":        "#3b82f6",
    "blue_lt":     "#1e3a5f",
    "blue_dk":     "#2563eb",
    "blue_xdk":    "#1d4ed8",
    # success
    "green":       "#22c55e",
    "green_lt":    "#14532d",
    "green_dk":    "#16a34a",
    "green_xdk":   "#15803d",
    # danger
    "red":         "#f87171",
    "red_lt":      "#450a0a",
    "red_dk":      "#ef4444",
    # text
    "txt":         "#e2e8f0",
    "txt2":        "#94a3b8",
    "txt3":        "#64748b",
    "txt4":        "#475569",
    # status
    "ok":          "#22c55e",
    "warn":        "#f59e0b",
}

# ─────────────────────────────────────────────────────────────────────────────
#  Theme palette registry
# ─────────────────────────────────────────────────────────────────────────────

THEMES = {
    "Slate Dark": {
        "bg":         "#1a1d23", "surface":  "#22262e", "surface2": "#2a2f39",
        "surface3":   "#313847", "border":   "#363c4a", "border_hi":"#3b82f6",
        "border_md":  "#454e5e", "blue":     "#3b82f6", "blue_lt":  "#1e3a5f",
        "blue_dk":    "#2563eb", "blue_xdk": "#1d4ed8", "green":    "#22c55e",
        "green_lt":   "#14532d", "green_dk": "#16a34a", "green_xdk":"#15803d",
        "red":        "#f87171", "red_lt":   "#450a0a", "red_dk":   "#ef4444",
        "txt":        "#e2e8f0", "txt2":     "#94a3b8", "txt3":     "#64748b",
        "txt4":       "#475569", "ok":       "#22c55e", "warn":     "#f59e0b",
    },
    "Midnight Blue": {
        "bg":         "#0d1117", "surface":  "#161b22", "surface2": "#21262d",
        "surface3":   "#2d333b", "border":   "#30363d", "border_hi":"#58a6ff",
        "border_md":  "#3d444d", "blue":     "#58a6ff", "blue_lt":  "#0d2137",
        "blue_dk":    "#1f6feb", "blue_xdk": "#1158c7", "green":    "#3fb950",
        "green_lt":   "#0d3b1f", "green_dk": "#238636", "green_xdk":"#1a7f37",
        "red":        "#ff7b72", "red_lt":   "#3d0f0f", "red_dk":   "#da3633",
        "txt":        "#c9d1d9", "txt2":     "#8b949e", "txt3":     "#6e7681",
        "txt4":       "#484f58", "ok":       "#3fb950", "warn":     "#d29922",
    },
    "Crimson Night": {
        "bg":         "#1a1118", "surface":  "#231520", "surface2": "#2d1a2a",
        "surface3":   "#382035", "border":   "#4a2a44", "border_hi":"#e05c8a",
        "border_md":  "#5e3558", "blue":     "#e05c8a", "blue_lt":  "#4a1030",
        "blue_dk":    "#c2185b", "blue_xdk": "#ad1457", "green":    "#4caf82",
        "green_lt":   "#0d3326", "green_dk": "#2e7d58", "green_xdk":"#1b5e40",
        "red":        "#ff6b8a", "red_lt":   "#4a0a1a", "red_dk":   "#e53935",
        "txt":        "#f3e5ee", "txt2":     "#c9a0bc", "txt3":     "#9e6e8e",
        "txt4":       "#6e4060", "ok":       "#4caf82", "warn":     "#ffb74d",
    },
    "Forest Green": {
        "bg":         "#0f1a10", "surface":  "#152018", "surface2": "#1e2e20",
        "surface3":   "#253828", "border":   "#2e4230", "border_hi":"#4caf50",
        "border_md":  "#3a5240", "blue":     "#4caf50", "blue_lt":  "#0d2e10",
        "blue_dk":    "#388e3c", "blue_xdk": "#2e7d32", "green":    "#81c784",
        "green_lt":   "#0d3b1a", "green_dk": "#388e3c", "green_xdk":"#2e7d32",
        "red":        "#ef9a9a", "red_lt":   "#3e1010", "red_dk":   "#e53935",
        "txt":        "#e8f5e9", "txt2":     "#a5d6a7", "txt3":     "#66bb6a",
        "txt4":       "#388e3c", "ok":       "#81c784", "warn":     "#ffcc02",
    },
    "Light Pro": {
        "bg":         "#f0f2f5", "surface":  "#ffffff", "surface2": "#f5f7fa",
        "surface3":   "#eaecf0", "border":   "#d0d7de", "border_hi":"#2563eb",
        "border_md":  "#b0b8c8", "blue":     "#2563eb", "blue_lt":  "#dbeafe",
        "blue_dk":    "#1d4ed8", "blue_xdk": "#1e40af", "green":    "#16a34a",
        "green_lt":   "#dcfce7", "green_dk": "#15803d", "green_xdk":"#166534",
        "red":        "#dc2626", "red_lt":   "#fee2e2", "red_dk":   "#b91c1c",
        "txt":        "#111827", "txt2":     "#374151", "txt3":     "#6b7280",
        "txt4":       "#9ca3af", "ok":       "#16a34a", "warn":     "#d97706",
    },
}

_CURRENT_THEME = "Slate Dark"

def apply_theme(name):
    global C, _CURRENT_THEME
    if name in THEMES:
        C.update(THEMES[name])
        _CURRENT_THEME = name

F_DISPLAY = ("Segoe UI Semibold",  9)
F_LABEL   = ("Segoe UI",           8)
F_LABELB  = ("Segoe UI Semibold",  8)
F_MONO    = ("Consolas",           8)
F_MONO_S  = ("Consolas",           7)
F_TITLE   = ("Segoe UI",          11, "bold")
F_CAP     = ("Segoe UI Semibold",  7)
F_BTN     = ("Segoe UI Semibold",  8)
F_MICRO   = ("Segoe UI",           7)


# ─────────────────────────────────────────────────────────────────────────────
#  FlatButton
# ─────────────────────────────────────────────────────────────────────────────

class FlatButton(tk.Frame):
    def __init__(self, master, text="", command=None,
                 bg_normal=None, bg_hover=None, bg_press=None,
                 fg=C["txt"], font=F_BTN,
                 padx=20, pady=7, **kw):
        super().__init__(master, bg=C["bg"], **kw)
        self._bg_n = bg_normal or C["surface2"]
        self._bg_h = bg_hover  or C["surface3"]
        self._bg_p = bg_press  or C["border"]
        self._fg   = fg
        self._tv   = tk.StringVar(value=text)

        self._b = tk.Button(
            self, textvariable=self._tv, command=command,
            bg=self._bg_n, fg=fg,
            activebackground=self._bg_h, activeforeground=fg,
            disabledforeground=C["txt4"],
            relief="flat", bd=0,
            font=font, padx=padx, pady=pady,
            cursor="hand2", highlightthickness=0, takefocus=0)
        self._b.pack(fill="both", expand=True)
        self._b.bind("<Enter>",          self._on_enter)
        self._b.bind("<Leave>",          self._on_leave)
        self._b.bind("<ButtonPress-1>",  self._on_press)
        self._b.bind("<ButtonRelease-1>",self._on_release)

    def configure(self, **kw):
        if "text"  in kw: self._tv.set(kw.pop("text"))
        if "state" in kw:
            st = kw.pop("state")
            self._b.configure(state=st,
                cursor="arrow" if st == "disabled" else "hand2")
        if kw: self._b.configure(**kw)

    def _on_enter(self, e):
        if str(self._b["state"]) != "disabled":
            self._b.configure(bg=self._bg_h)
    def _on_leave(self, e):
        if str(self._b["state"]) != "disabled":
            self._b.configure(bg=self._bg_n)
    def _on_press(self, e):
        if str(self._b["state"]) != "disabled":
            self._b.configure(bg=self._bg_p)
    def _on_release(self, e):
        if str(self._b["state"]) != "disabled":
            self._b.configure(bg=self._bg_h)


# ─────────────────────────────────────────────────────────────────────────────
#  HistoryEntry
# ─────────────────────────────────────────────────────────────────────────────

class HistoryEntry(tk.Frame):
    def __init__(self, master, items=None, show="", **kw):
        super().__init__(master, bg=C["surface"], **kw)
        self._items = list(items or [])
        self._show  = show
        self._popup = None
        self.columnconfigure(0, weight=1)

        # border frame
        self._border = tk.Frame(self, bg=C["border"],
                                highlightthickness=0)
        self._border.grid(row=0, column=0, columnspan=2, sticky="ew")
        self._border.columnconfigure(0, weight=1)

        self.var = tk.StringVar()
        self._e  = tk.Entry(self._border, textvariable=self.var,
                            show=show, font=F_MONO,
                            bg=C["surface2"], fg=C["txt"],
                            insertbackground=C["blue"],
                            selectbackground=C["blue_lt"],
                            selectforeground=C["blue"],
                            relief="flat", bd=0)
        self._e.grid(row=0, column=0, sticky="ew",
                     padx=1, pady=1, ipady=6)

        self._arrow = tk.Label(self._border, text="▾",
                               font=("Segoe UI", 8),
                               bg=C["surface2"], fg=C["txt4"],
                               cursor="hand2", padx=8)
        self._arrow.grid(row=0, column=1, sticky="ns",
                         padx=(0, 1), pady=1)
        self._arrow.bind("<Button-1>", lambda e: self._toggle())
        self._arrow.bind("<Enter>",    lambda e: self._arrow.configure(fg=C["blue"]))
        self._arrow.bind("<Leave>",    lambda e: self._arrow.configure(fg=C["txt4"]))

        self._e.bind("<FocusIn>",  lambda e: self._border.configure(bg=C["border_hi"]))
        self._e.bind("<FocusOut>", lambda e: self._border.configure(bg=C["border"]))
        self.bind_all("<Button-1>", self._on_global_click)

    def get(self)          -> str: return self.var.get()
    def set(self, v: str):         self.var.set(v)
    def update_items(self, items): self._items = list(items)

    def _toggle(self):
        if self._popup and self._popup.winfo_exists(): self._close()
        elif self._items: self._open()

    def _open(self):
        self._close()
        pop = tk.Toplevel(self)
        pop.overrideredirect(True)
        pop.configure(bg=C["border_hi"])
        self._popup = pop

        self.update_idletasks()
        rx = self.winfo_rootx()
        ry = self.winfo_rooty() + self.winfo_height()
        rw = self.winfo_width()

        ITEM_H  = 30
        visible = min(len(self._items), 7)

        shell = tk.Frame(pop, bg=C["surface"],
                         highlightbackground=C["border_hi"],
                         highlightthickness=1)
        shell.pack(fill="both", expand=True)

        cv = tk.Canvas(shell, bg=C["surface"], bd=0,
                       highlightthickness=0,
                       width=rw - 2, height=visible * ITEM_H)
        cv.pack(side="left", fill="both", expand=True)

        sb = tk.Scrollbar(shell, orient="vertical", command=cv.yview,
                          bg=C["surface2"], troughcolor=C["surface3"],
                          bd=0, width=8)
        if len(self._items) > visible: sb.pack(side="right", fill="y")
        cv.configure(yscrollcommand=sb.set)

        inner = tk.Frame(cv, bg=C["surface"])
        wid   = cv.create_window((0, 0), window=inner, anchor="nw")
        inner.bind("<Configure>",
                   lambda e: (cv.configure(scrollregion=cv.bbox("all")),
                               cv.itemconfig(wid, width=cv.winfo_width())))

        for i, item in enumerate(self._items):
            label = ("*" * min(len(item), 16)) if self._show else item
            # alternating row tint
            row_bg = C["surface"] if i % 2 == 0 else C["surface3"]
            fr = tk.Frame(inner, bg=row_bg, cursor="hand2")
            fr.pack(fill="x")

            # left accent bar (hidden until hover)
            bar = tk.Frame(fr, bg=row_bg, width=3)
            bar.pack(side="left", fill="y")

            lb = tk.Label(fr, text=label, font=F_MONO,
                          bg=row_bg, fg=C["txt2"],
                          anchor="w", padx=8, pady=5)
            lb.pack(side="left", fill="x", expand=True)

            def _sel(v=item):         self.set(v); self._close()
            def _ent(e, f=fr, l=lb, b=bar, rbg=row_bg):
                f.configure(bg=C["blue_lt"]); l.configure(bg=C["blue_lt"], fg=C["blue"])
                b.configure(bg=C["blue"])
            def _lv(e, f=fr, l=lb, b=bar, rbg=row_bg):
                f.configure(bg=rbg); l.configure(bg=rbg, fg=C["txt2"])
                b.configure(bg=rbg)

            for w in (fr, lb, bar):
                w.bind("<Button-1>", lambda e, s=_sel: s())
                w.bind("<Enter>", _ent); w.bind("<Leave>", _lv)

        pop.geometry(f"{rw}+{rx}+{ry}")
        pop.lift()

    def _close(self):
        if self._popup and self._popup.winfo_exists(): self._popup.destroy()
        self._popup = None

    def _on_global_click(self, event):
        if not (self._popup and self._popup.winfo_exists()): return
        px, py = self._popup.winfo_rootx(), self._popup.winfo_rooty()
        pw, ph = self._popup.winfo_width(),  self._popup.winfo_height()
        if not (px <= event.x_root <= px + pw and
                py <= event.y_root <= py + ph):
            self._close()


# ─────────────────────────────────────────────────────────────────────────────
#  Main application
# ─────────────────────────────────────────────────────────────────────────────

class SignToolGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Digital Code Signature Lite — polsoft.ITS™")
        self.resizable(True, False)
        self.configure(bg=C["bg"])

        # Set window icon from embedded logo
        try:
            _ico = _get_logo_image(32)
            if _ico:
                self.iconphoto(True, _ico)
                self._wm_icon = _ico  # keep reference
        except Exception:
            pass

        self._signtool = find_signtool()
        self.history   = load_history()
        self._lang     = "en"

        self._theme()
        self._build()
        self._autosize()

    def _(self, key, **kw):
        t = TRANSLATIONS[self._lang].get(key, key)
        return t.format(**kw) if kw else t

    def _autosize(self):
        self.update_idletasks()
        w = self.winfo_reqwidth()
        h = self.winfo_reqheight()
        sw, sh = self.winfo_screenwidth(), self.winfo_screenheight()
        self.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")
        self.minsize(w, h)

    def _theme(self):
        s = ttk.Style(self)
        s.theme_use("default")
        s.configure("TCheckbutton",
                    background=C["surface"], foreground=C["txt3"],
                    font=F_LABEL, focuscolor="")
        s.map("TCheckbutton",
              background=[("active", C["surface"])],
              foreground=[("active", C["blue"])])
        s.configure("TCombobox",
                    fieldbackground=C["surface2"],
                    background=C["surface2"],
                    foreground=C["txt"],
                    selectbackground=C["blue_lt"],
                    selectforeground=C["blue"],
                    arrowcolor=C["txt3"],
                    bordercolor=C["border"],
                    lightcolor=C["border"],
                    darkcolor=C["border"])
        s.map("TCombobox",
              fieldbackground=[("readonly", C["surface2"])],
              foreground=[("readonly", C["txt"])])

    # ── build ─────────────────────────────────────────────────────────────────

    def _build(self):
        self.columnconfigure(0, weight=1)
        self._build_header()
        self._build_body()
        self._build_footer()

    # ── header ────────────────────────────────────────────────────────────────

    def _build_header(self):
        hdr = tk.Frame(self, bg=C["surface"],
                       highlightbackground=C["border"],
                       highlightthickness=1)
        hdr.grid(row=0, column=0, sticky="ew")
        hdr.columnconfigure(1, weight=1)

        # top blue stripe
        tk.Frame(hdr, bg=C["blue"], height=3).grid(
            row=0, column=0, columnspan=3, sticky="ew")

        # left: icon + branding
        left = tk.Frame(hdr, bg=C["surface"])
        left.grid(row=1, column=0, padx=(12, 10), pady=(7, 7), sticky="w")

        # real logo image
        self._logo_img = _get_logo_image(40)
        if self._logo_img:
            icon_box = tk.Frame(left, bg=C["surface"])
            icon_box.pack(side="left", padx=(0, 10))
            tk.Label(icon_box, image=self._logo_img,
                     bg=C["surface"], bd=0).pack()
        else:
            icon_box = tk.Frame(left, bg=C["blue_lt"],
                                highlightbackground=C["border_hi"],
                                highlightthickness=1)
            icon_box.pack(side="left", padx=(0, 10))
            tk.Label(icon_box, text="🔐",
                     font=("Segoe UI Emoji", 14),
                     bg=C["blue_lt"], fg=C["blue"],
                     padx=7, pady=5).pack()

        # title block
        titles = tk.Frame(left, bg=C["surface"])
        titles.pack(side="left")
        tk.Label(titles, text="Digital Code Signature Lite",
                 font=F_TITLE, bg=C["surface"], fg=C["txt"]).pack(anchor="w")
        self._lbl_subtitle = tk.Label(
            titles, text=self._("app_subtitle"),
            font=F_MICRO, bg=C["surface"], fg=C["txt3"])
        self._lbl_subtitle.pack(anchor="w", pady=(1, 0))

        # divider
        tk.Frame(hdr, bg=C["border"], width=1).grid(
            row=1, column=1, sticky="ns", pady=6)

        # right: controls
        right = tk.Frame(hdr, bg=C["surface"])
        right.grid(row=1, column=2, padx=(10, 12), sticky="e")

        # language button
        self._btn_lang = tk.Button(
            right, text=self._("btn_lang"),
            command=self._toggle_lang,
            bg=C["surface3"], fg=C["blue"],
            activebackground=C["blue_lt"],
            activeforeground=C["blue_dk"],
            relief="flat", bd=0,
            font=F_MICRO, padx=7, pady=2,
            cursor="hand2", highlightthickness=0)
        self._btn_lang.pack(anchor="e", pady=(0, 5))

        # signtool status badge
        ok      = bool(self._signtool)
        bg_b    = C["green_lt"] if ok else C["red_lt"]
        fg_b    = C["green"]    if ok else C["red"]
        st_name = os.path.basename(self._signtool) if self._signtool else ""
        st_txt  = (self._("st_found", name=st_name)
                   if ok else self._("st_missing"))

        badge = tk.Frame(right, bg=bg_b,
                         highlightbackground=fg_b,
                         highlightthickness=1)
        badge.pack(anchor="e")
        tk.Label(badge, text="●", font=("Segoe UI", 5),
                 bg=bg_b, fg=fg_b).pack(side="left", padx=(5, 1), pady=3)
        self._lbl_st = tk.Label(badge, text=st_txt,
                                font=F_MONO_S, bg=bg_b, fg=fg_b)
        self._lbl_st.pack(side="left", padx=(0, 6), pady=3)
        self._st_badge    = badge
        self._st_badge_bg = bg_b
        self._st_badge_fg = fg_b

        tk.Label(right, text=f"v{__version__}",
                 font=F_MICRO, bg=C["surface"],
                 fg=C["txt4"]).pack(anchor="e", pady=(4, 0))

        # bottom rule
        tk.Frame(hdr, bg=C["border"], height=1).grid(
            row=2, column=0, columnspan=3, sticky="ew")

    # ── body ──────────────────────────────────────────────────────────────────

    def _build_body(self):
        body = tk.Frame(self, bg=C["bg"])
        body.grid(row=1, column=0, sticky="ew")
        body.columnconfigure(0, weight=1)

        # main card
        card = tk.Frame(body, bg=C["surface"],
                        highlightbackground=C["border"],
                        highlightthickness=1)
        card.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        card.columnconfigure(1, weight=1)

        # ── file ─────────────────────────────────────────────────────────────
        self._sep_file = self._sec(card, self._("sec_file"), 0)

        self._lbl_file = self._rlabel(card, self._("lbl_file"), 1)
        self.he_file   = HistoryEntry(card, items=self.history.get("files", []))
        self.he_file.grid(row=1, column=1, sticky="ew", padx=(0, 0), pady=2)
        self._bbf = self._browse_btn(card,
            lambda: self._browse(self.he_file,
                self._("browse_file_title"),
                [(self._("browse_ft_binary"), "*.exe *.dll *.msi *.cab *.appx"),
                 (self._("browse_ft_all"), "*.*")], "files"), 1)

        # ── certificate ───────────────────────────────────────────────────────
        self._sep_cert = self._sec(card, self._("sec_cert"), 2)

        self._lbl_cert = self._rlabel(card, self._("lbl_cert"), 3)
        self.he_cert   = HistoryEntry(card, items=self.history.get("certs", []))
        self.he_cert.grid(row=3, column=1, sticky="ew", pady=2)
        self._bbc = self._browse_btn(card,
            lambda: self._browse(self.he_cert,
                self._("browse_cert_title"),
                [(self._("browse_ft_cert"), "*.pfx *.p12"),
                 (self._("browse_ft_all"), "*.*")], "certs"), 3)

        self._lbl_pass = self._rlabel(card, self._("lbl_password"), 4)
        pw = tk.Frame(card, bg=C["surface"])
        pw.grid(row=4, column=1, columnspan=2, sticky="ew",
                pady=2, padx=(0, 10))
        pw.columnconfigure(0, weight=1)

        self.he_pass = HistoryEntry(pw, items=self.history.get("passwords", []),
                                    show="*")
        self.he_pass.grid(row=0, column=0, sticky="ew")

        self.var_showp  = tk.BooleanVar(value=False)
        self._chk_showp = ttk.Checkbutton(
            pw, text=self._("lbl_show_pass"),
            variable=self.var_showp,
            command=self._toggle_pass,
            style="Surface.TCheckbutton")
        self._chk_showp.grid(row=0, column=1, padx=(10, 0))

        # ── advanced ─────────────────────────────────────────────────────────
        self._sep_adv = self._sec(card, self._("sec_advanced"), 5)

        # subtle tinted row
        adv_bg = tk.Frame(card, bg=C["surface3"])
        adv_bg.grid(row=6, column=0, columnspan=3, sticky="ew",
                    padx=1, pady=(2, 10))
        adv_bg.columnconfigure(1, weight=1)

        self.var_ts    = tk.BooleanVar(value=True)
        self.var_tsurl = tk.StringVar(value="http://timestamp.sectigo.com")
        self.var_hash  = tk.StringVar(value="sha256")

        # re-style checkbutton for adv_bg
        s = ttk.Style(self)
        s.configure("Adv.TCheckbutton",
                    background=C["surface3"], foreground=C["txt3"],
                    font=F_LABEL, focuscolor="")
        s.map("Adv.TCheckbutton",
              background=[("active", C["surface3"])],
              foreground=[("active", C["blue"])])

        self._chk_ts = ttk.Checkbutton(adv_bg, text=self._("lbl_timestamp"),
                                        variable=self.var_ts,
                                        style="Adv.TCheckbutton")
        self._chk_ts.grid(row=0, column=0, sticky="w", padx=(8, 6), pady=5)

        ts_f = tk.Frame(adv_bg, bg=C["border"])
        ts_f.grid(row=0, column=1, sticky="ew", padx=(0, 8), pady=5)
        ts_f.columnconfigure(0, weight=1)
        tk.Entry(ts_f, textvariable=self.var_tsurl,
                 font=F_MONO, bg=C["surface2"], fg=C["txt"],
                 insertbackground=C["blue"],
                 relief="flat", bd=0).grid(
            row=0, column=0, sticky="ew", padx=1, pady=1, ipady=3)

        self._lbl_alg = tk.Label(adv_bg, text=self._("lbl_algorithm"),
                                  font=F_LABELB,
                                  bg=C["surface3"], fg=C["txt3"])
        self._lbl_alg.grid(row=1, column=0, sticky="w",
                           padx=(8, 6), pady=(0, 5))
        ttk.Combobox(adv_bg, textvariable=self.var_hash,
                     values=["sha256", "sha384", "sha512"],
                     state="readonly", width=10, font=F_MONO).grid(
            row=1, column=1, sticky="w", padx=(0, 8), pady=(0, 5))

        # ── action buttons ────────────────────────────────────────────────────
        btn_row = tk.Frame(body, bg=C["bg"])
        btn_row.grid(row=1, column=0, sticky="ew", padx=10, pady=(0, 10))
        btn_row.columnconfigure(0, weight=1)

        right_btns = tk.Frame(btn_row, bg=C["bg"])
        right_btns.grid(row=0, column=1)

        self.btn_cancel = FlatButton(
            right_btns, text=self._("btn_cancel"),
            command=self._on_cancel,
            bg_normal=C["red_lt"],
            bg_hover=C["red_dk"],
            bg_press=C["red"],
            fg=C["red"],
            font=F_BTN, padx=16, pady=5)
        self.btn_cancel.pack(side="right", padx=(6, 0))

        self.btn_sign = FlatButton(
            right_btns, text=self._("btn_sign"),
            command=self._on_sign,
            bg_normal=C["blue"],
            bg_hover=C["blue_dk"],
            bg_press=C["blue_xdk"],
            fg="#ffffff",
            font=F_BTN, padx=20, pady=5)
        self.btn_sign.pack(side="right")

        self.btn_verify = FlatButton(
            right_btns, text=self._("btn_verify"),
            command=self._on_verify,
            bg_normal=C["green_lt"],
            bg_hover=C["green_dk"],
            bg_press=C["green_xdk"],
            fg=C["green"],
            font=F_BTN, padx=16, pady=5)
        self.btn_verify.pack(side="right", padx=(0, 6))

    # ── footer ────────────────────────────────────────────────────────────────

    def _build_footer(self):
        ft = tk.Frame(self, bg=C["surface"],
                      highlightbackground=C["border"],
                      highlightthickness=1)
        ft.grid(row=2, column=0, sticky="ew")
        ft.columnconfigure(3, weight=1)

        # broom icon button (clear history)
        self._btn_clear = tk.Button(
            ft, text="🧹",
            command=self._clear_history,
            bg=C["surface"], fg=C["txt3"],
            activebackground=C["red_lt"],
            activeforeground=C["red"],
            relief="flat", bd=0,
            font=("Segoe UI Emoji", 11), padx=6, pady=2,
            cursor="hand2", highlightthickness=0)
        self._btn_clear.grid(row=0, column=0, sticky="w",
                             padx=(6, 2), pady=4)
        self._btn_clear.bind("<Enter>", lambda e: self._btn_clear.configure(fg=C["red"]))
        self._btn_clear.bind("<Leave>", lambda e: self._btn_clear.configure(fg=C["txt3"]))

        # themes icon button
        self._btn_themes = tk.Button(
            ft, text="🎨",
            command=self._show_themes,
            bg=C["surface"], fg=C["txt3"],
            activebackground=C["surface2"],
            activeforeground=C["blue"],
            relief="flat", bd=0,
            font=("Segoe UI Emoji", 11), padx=6, pady=2,
            cursor="hand2", highlightthickness=0)
        self._btn_themes.grid(row=0, column=1, sticky="w",
                              padx=(0, 2), pady=4)
        self._btn_themes.bind("<Enter>", lambda e: self._btn_themes.configure(fg=C["blue"]))
        self._btn_themes.bind("<Leave>", lambda e: self._btn_themes.configure(fg=C["txt3"]))

        # about icon button
        self._btn_about = tk.Button(
            ft, text="ℹ",
            command=self._show_about,
            bg=C["surface"], fg=C["txt3"],
            activebackground=C["blue_lt"],
            activeforeground=C["blue"],
            relief="flat", bd=0,
            font=("Segoe UI", 12, "bold"), padx=6, pady=2,
            cursor="hand2", highlightthickness=0)
        self._btn_about.grid(row=0, column=2, sticky="w",
                              padx=(0, 0), pady=4)
        self._btn_about.bind("<Enter>", lambda e: self._btn_about.configure(fg=C["blue"]))
        self._btn_about.bind("<Leave>", lambda e: self._btn_about.configure(fg=C["txt3"]))

        tk.Label(ft,
                 text=f"{__copyright__}  •  {__email__}",
                 font=F_MICRO, bg=C["surface"],
                 fg=C["txt2"]).grid(
            row=0, column=3, sticky="e", padx=(0, 10), pady=4)

    def _show_about(self):
        win = tk.Toplevel(self)
        win.title("About Digital Code Signature Lite")
        win.resizable(False, False)
        win.configure(bg=C["bg"])
        win.grab_set()

        # center over parent
        self.update_idletasks()
        px, py = self.winfo_rootx(), self.winfo_rooty()
        pw, ph = self.winfo_width(), self.winfo_height()
        win.update_idletasks()
        ww, wh = 420, 380
        win.geometry(f"{ww}x{wh}+{px+(pw-ww)//2}+{py+(ph-wh)//2}")

        # top blue stripe
        tk.Frame(win, bg=C["blue"], height=3).pack(fill="x")

        # centered logo + title block
        top = tk.Frame(win, bg=C["surface"], pady=18)
        top.pack(fill="x")
        img = _get_logo_image(56)
        if img:
            lbl_img = tk.Label(top, image=img, bg=C["surface"])
            lbl_img.image = img
            lbl_img.pack(anchor="center")
        tk.Label(top, text="Digital Code Signature Lite",
                 font=("Segoe UI", 18, "bold"),
                 bg=C["surface"], fg=C["txt"]).pack(anchor="center", pady=(8, 2))
        tk.Label(top, text=f"Version {__version__}",
                 font=("Segoe UI", 9),
                 bg=C["surface"], fg=C["txt3"]).pack(anchor="center")

        tk.Frame(win, bg=C["border"], height=1).pack(fill="x")

        # info area
        body = tk.Frame(win, bg=C["bg"], padx=20, pady=14)
        body.pack(fill="both", expand=True)

        # polsoft.ITS section
        sec1 = tk.Frame(body, bg=C["surface2"],
                        highlightbackground=C["border"], highlightthickness=1)
        sec1.pack(fill="x", pady=(0, 10))
        tk.Label(sec1, text="  Application Author",
                 font=("Segoe UI Semibold", 8),
                 bg=C["surface2"], fg=C["blue"],
                 anchor="w").pack(fill="x", padx=8, pady=(8, 2))
        tk.Label(sec1, text=f"  {__author__}  ·  {__company__}",
                 font=("Segoe UI", 9),
                 bg=C["surface2"], fg=C["txt"],
                 anchor="w").pack(fill="x", padx=8)
        tk.Label(sec1, text=f"  {__email__}",
                 font=("Consolas", 8),
                 bg=C["surface2"], fg=C["txt3"],
                 anchor="w").pack(fill="x", padx=8)
        tk.Label(sec1, text=f"  {__github__}",
                 font=("Consolas", 8),
                 bg=C["surface2"], fg=C["txt3"],
                 anchor="w").pack(fill="x", padx=8, pady=(0, 8))

        # Microsoft section
        sec2 = tk.Frame(body, bg=C["surface2"],
                        highlightbackground=C["border"], highlightthickness=1)
        sec2.pack(fill="x")
        tk.Label(sec2, text="  signtool.exe Provider",
                 font=("Segoe UI Semibold", 8),
                 bg=C["surface2"], fg=C["blue"],
                 anchor="w").pack(fill="x", padx=8, pady=(8, 2))
        tk.Label(sec2, text="  Microsoft Corporation  ·  Windows SDK (10/11)",
                 font=("Segoe UI", 9),
                 bg=C["surface2"], fg=C["txt"],
                 anchor="w").pack(fill="x", padx=8)
        tk.Label(sec2, text="  https://developer.microsoft.com/en-us/windows/downloads/windows-sdk/",
                 font=("Consolas", 7),
                 bg=C["surface2"], fg=C["txt3"],
                 anchor="w").pack(fill="x", padx=8, pady=(0, 8))

        tk.Frame(win, bg=C["border"], height=1).pack(fill="x")

        # close button
        tk.Button(win, text="Close",
                  command=win.destroy,
                  bg=C["blue"], fg="#ffffff",
                  activebackground=C["blue_dk"],
                  activeforeground="#ffffff",
                  relief="flat", bd=0,
                  font=("Segoe UI Semibold", 9),
                  padx=22, pady=6,
                  cursor="hand2", highlightthickness=0).pack(
            anchor="e", padx=18, pady=10)

    def _show_themes(self):
        win = tk.Toplevel(self)
        win.title("Themes")
        win.resizable(False, False)
        win.configure(bg=C["bg"])
        win.grab_set()

        self.update_idletasks()
        px, py = self.winfo_rootx(), self.winfo_rooty()
        pw, ph = self.winfo_width(), self.winfo_height()
        win.update_idletasks()
        ww, wh = 340, 310
        win.geometry(f"{ww}x{wh}+{px+(pw-ww)//2}+{py+(ph-wh)//2}")

        tk.Frame(win, bg=C["blue"], height=3).pack(fill="x")

        hdr = tk.Frame(win, bg=C["surface"], pady=10)
        hdr.pack(fill="x")
        tk.Label(hdr, text="🎨  Choose Theme",
                 font=("Segoe UI Semibold", 11),
                 bg=C["surface"], fg=C["txt"]).pack(anchor="center")

        tk.Frame(win, bg=C["border"], height=1).pack(fill="x")

        body = tk.Frame(win, bg=C["bg"], padx=16, pady=12)
        body.pack(fill="both", expand=True)

        # color swatch previews for each theme
        SWATCHES = {
            "Slate Dark":    ["#1a1d23", "#3b82f6", "#22c55e", "#f87171"],
            "Midnight Blue": ["#0d1117", "#58a6ff", "#3fb950", "#ff7b72"],
            "Crimson Night": ["#1a1118", "#e05c8a", "#4caf82", "#ff6b8a"],
            "Forest Green":  ["#0f1a10", "#4caf50", "#81c784", "#ef9a9a"],
            "Light Pro":     ["#f0f2f5", "#2563eb", "#16a34a", "#dc2626"],
        }

        for theme_name, swatches in SWATCHES.items():
            row = tk.Frame(body, bg=C["surface2"],
                           highlightbackground=C["border_hi"] if theme_name == _CURRENT_THEME else C["border"],
                           highlightthickness=1)
            row.pack(fill="x", pady=3)
            row.columnconfigure(1, weight=1)

            # swatches
            sw_frame = tk.Frame(row, bg=C["surface2"])
            sw_frame.grid(row=0, column=0, padx=(8, 6), pady=7)
            for color in swatches:
                tk.Frame(sw_frame, bg=color, width=12, height=12,
                         highlightbackground="#222222",
                         highlightthickness=1).pack(side="left", padx=1)

            tk.Label(row, text=theme_name,
                     font=("Segoe UI Semibold", 9),
                     bg=C["surface2"],
                     fg=C["blue"] if theme_name == _CURRENT_THEME else C["txt"]).grid(
                row=0, column=1, sticky="w")

            active_lbl = tk.Label(row, text="✓ active" if theme_name == _CURRENT_THEME else "",
                                  font=("Segoe UI", 7),
                                  bg=C["surface2"], fg=C["green"])
            active_lbl.grid(row=0, column=2, padx=(0, 8))

            def _apply(tn=theme_name):
                apply_theme(tn)
                self._rebuild_ui()
                win.destroy()

            row.bind("<Button-1>", lambda e, fn=_apply: fn())
            for child in row.winfo_children():
                child.bind("<Button-1>", lambda e, fn=_apply: fn())
            row.bind("<Enter>", lambda e, r=row: r.configure(highlightbackground=C["border_hi"]))
            row.bind("<Leave>", lambda e, r=row, tn=theme_name: r.configure(
                highlightbackground=C["border_hi"] if tn == _CURRENT_THEME else C["border"]))

        tk.Frame(win, bg=C["border"], height=1).pack(fill="x")
        tk.Button(win, text="Cancel", command=win.destroy,
                  bg=C["surface"], fg=C["txt2"],
                  activebackground=C["surface2"], activeforeground=C["txt"],
                  relief="flat", bd=0, font=("Segoe UI Semibold", 9),
                  padx=18, pady=5, cursor="hand2", highlightthickness=0).pack(
            anchor="e", padx=16, pady=8)

    def _rebuild_ui(self):
        """Destroy and rebuild all widgets with updated C palette."""
        for widget in self.winfo_children():
            widget.destroy()
        self._theme()
        self._build()

    # ── verify ────────────────────────────────────────────────────────────────

    def _on_verify(self):
        ft = self.he_file.get().strip()
        if not ft:
            messagebox.showwarning(self._("title_error"), self._("verify_no_file"))
            return
        if not self._signtool:
            messagebox.showerror(self._("title_error"), self._("err_no_signtool"))
            return
        self.btn_verify.configure(state="disabled", text=self._("btn_verifying"))
        threading.Thread(target=self._run_verify, daemon=True).start()

    def _run_verify(self):
        ft = self.he_file.get().strip()
        cmd = [self._signtool, "verify", "/pa", "/v", ft]

        def done(ok, msg):
            self.btn_verify.configure(state="normal", text=self._("btn_verify"))
            (messagebox.showinfo if ok else messagebox.showerror)(
                self._("title_success" if ok else "title_error"), msg)

        try:
            si = subprocess.STARTUPINFO()
            si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            si.wShowWindow = 0  # SW_HIDE
            r = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                startupinfo=si,
                creationflags=subprocess.CREATE_NO_WINDOW,
            )
            detail = (r.stdout + "\n" + r.stderr).strip()[:500]
            if r.returncode == 0:
                self.after(0, lambda: done(True, self._("verify_ok", detail=detail)))
            else:
                self.after(0, lambda: done(
                    False, self._("verify_fail", code=r.returncode, detail=detail)))
        except FileNotFoundError:
            self.after(0, lambda: done(
                False, self._("verify_not_found", path=self._signtool)))
        except Exception as exc:
            self.after(0, lambda: done(False, str(exc)))

    def _sec(self, parent, label, row):
        f = tk.Frame(parent, bg=C["surface"])
        f.grid(row=row, column=0, columnspan=3, sticky="ew",
               padx=10, pady=(10, 2))
        f.columnconfigure(1, weight=1)
        lbl = tk.Label(f, text=label, font=F_CAP,
                       bg=C["surface"], fg=C["blue"])
        lbl.grid(row=0, column=0, sticky="w", padx=(2, 6))
        tk.Frame(f, bg=C["border_hi"], height=1).grid(
            row=0, column=1, sticky="ew")
        f._lbl = lbl
        return f

    def _rlabel(self, parent, text, row):
        l = tk.Label(parent, text=text, font=F_LABELB,
                     bg=C["surface"], fg=C["txt2"])
        l.grid(row=row, column=0, sticky="w", padx=(12, 8), pady=2)
        return l

    def _browse_btn(self, parent, cmd, row):
        b = tk.Button(parent, text="Browse", command=cmd,
                      bg=C["surface3"], fg=C["blue"],
                      activebackground=C["blue_lt"],
                      activeforeground=C["blue_dk"],
                      relief="flat", bd=0,
                      font=F_BTN, padx=8, pady=3,
                      cursor="hand2", highlightthickness=0)
        b.grid(row=row, column=2, padx=(4, 10), pady=2, sticky="ew")
        return b

    # ── i18n ─────────────────────────────────────────────────────────────────

    def _toggle_lang(self):
        self._lang = "pl" if self._lang == "en" else "en"
        self._retranslate()

    def _retranslate(self):
        self._lbl_subtitle.configure(text=self._("app_subtitle"))
        self._btn_lang.configure(text=self._("btn_lang"))
        st_name = os.path.basename(self._signtool) if self._signtool else ""
        self._lbl_st.configure(
            text=(self._("st_found", name=st_name)
                  if self._signtool else self._("st_missing")))
        for frm, key in [(self._sep_file, "sec_file"),
                          (self._sep_cert, "sec_cert"),
                          (self._sep_adv,  "sec_advanced")]:
            frm._lbl.configure(text=self._(key))
        self._lbl_file.configure(text=self._("lbl_file"))
        self._lbl_cert.configure(text=self._("lbl_cert"))
        self._lbl_pass.configure(text=self._("lbl_password"))
        self._chk_showp.configure(text=self._("lbl_show_pass"))
        self._chk_ts.configure(text=self._("lbl_timestamp"))
        self._lbl_alg.configure(text=self._("lbl_algorithm"))
        self.btn_sign.configure(text=self._("btn_sign"))
        self.btn_verify.configure(text=self._("btn_verify"))
        self.btn_cancel.configure(text=self._("btn_cancel"))

    # ── events ────────────────────────────────────────────────────────────────

    def _toggle_pass(self):
        sh = "" if self.var_showp.get() else "*"
        self.he_pass._e.configure(show=sh)
        self.he_pass._show = sh

    def _browse(self, widget, title, filetypes, key):
        path = filedialog.askopenfilename(title=title, filetypes=filetypes)
        if path:
            widget.set(path)
            self.history[key] = push_history(self.history.get(key, []), path)
            widget.update_items(self.history[key])
            save_history(self.history)

    def _clear_history(self):
        if not messagebox.askyesno(self._("clear_title"),
                                   self._("clear_confirm")): return
        self.history = {"certs": [], "passwords": [], "files": []}
        save_history(self.history)
        for w in (self.he_cert, self.he_pass, self.he_file):
            w.update_items([])
        messagebox.showinfo(self._("clear_done_title"),
                            self._("clear_done_msg"))

    # ── validation ────────────────────────────────────────────────────────────

    def _validate(self):
        if not self._signtool:
            messagebox.showerror(self._("title_error"),
                                 self._("err_no_signtool"))
            return False
        errors = []
        ft = self.he_file.get().strip()
        ct = self.he_cert.get().strip()
        if not ft:                   errors.append(self._("err_no_file"))
        elif not os.path.isfile(ft): errors.append(self._("err_file_missing", path=ft))
        if not ct:                   errors.append(self._("err_no_cert"))
        elif not os.path.isfile(ct): errors.append(self._("err_cert_missing", path=ct))
        if errors:
            messagebox.showerror(self._("err_title"), "\n".join(errors))
            return False
        if not self.he_pass.get():
            return messagebox.askyesno(self._("warn_no_pass_title"),
                                       self._("warn_no_pass_msg"))
        return True

    # ── actions ───────────────────────────────────────────────────────────────

    def _on_cancel(self):
        if messagebox.askyesno(self._("quit_title"),
                               self._("quit_confirm")):
            self.destroy()

    def _on_sign(self):
        if not self._validate(): return
        for val, key, widget in [
            (self.he_cert.get(), "certs",     self.he_cert),
            (self.he_pass.get(), "passwords", self.he_pass),
            (self.he_file.get(), "files",     self.he_file),
        ]:
            if val.strip():
                self.history[key] = push_history(self.history.get(key, []), val)
                widget.update_items(self.history[key])
        save_history(self.history)
        self.btn_sign.configure(state="disabled", text=self._("btn_signing"))
        threading.Thread(target=self._run, daemon=True).start()

    def _run(self):
        cmd = [self._signtool, "sign",
               "/f", self.he_cert.get().strip(),
               "/p", self.he_pass.get(),
               "/fd", self.var_hash.get(), "/v"]
        if self.var_ts.get() and self.var_tsurl.get().strip():
            cmd += ["/tr", self.var_tsurl.get().strip(),
                    "/td", self.var_hash.get()]
        cmd.append(self.he_file.get().strip())

        def done(ok, msg):
            self.btn_sign.configure(state="normal", text=self._("btn_sign"))
            (messagebox.showinfo if ok else messagebox.showerror)(
                self._("title_success" if ok else "title_error"), msg)

        try:
            si = subprocess.STARTUPINFO()
            si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            si.wShowWindow = 0  # SW_HIDE
            r = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                startupinfo=si,
                creationflags=subprocess.CREATE_NO_WINDOW,
            )
            if r.returncode == 0:
                self.after(0, lambda: done(True, self._("sign_ok")))
            else:
                detail = (r.stdout + "\n" + r.stderr).strip()[:500]
                self.after(0, lambda: done(
                    False, self._("sign_fail", code=r.returncode, detail=detail)))
        except FileNotFoundError:
            self.after(0, lambda: done(
                False, self._("sign_not_found", path=self._signtool)))
        except Exception as exc:
            self.after(0, lambda: done(False, str(exc)))


# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    app = SignToolGUI()
    app.mainloop()
