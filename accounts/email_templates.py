def HomePageCATEmailTemplate():
    return"""
    <!DOCTYPE html>
<html>

<head>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f7f7f7;
            color: #333;
            padding: 20px;
        }

        p {
            font-size: 18px;
            line-height: 1.6;
            margin: 10px 0;
        }

        .container {
            background-color: #ffffff;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            max-width: 600px;
            margin: auto;
        }

        .header {
            background-color: #483BBF;
            color: #ffffff;
            padding: 25px 0;
            text-align: center;
            border-radius: 10px 10px 0 0;
        }

        .content {
            margin: 30px 0;
        }

        ul {
            margin: 10px 0;
            padding-left: 20px;
        }

        li {
            margin-bottom: 10px;
            font-size: 18px;
        }

        img {
            max-width: 200px;
            height: auto;
        }

        .button {
            display: inline-block;
            padding: 10px 20px;
            color: #ffffff;
            background-color: #483BBF;
            text-align: center;
            border-radius: 5px;
            text-decoration: none;
            font-size: 16px;
        }

        .footer {
            margin-top: 20px;
            font-size: 12px;
            color: #999;
            text-align: center;
        }
    </style>
</head>

<body>
    <div class="container">
        <div class="header">
            <img src="https://res.cloudinary.com/dl8ppbbgu/image/upload/v1721162465/nv1w8ek2vgjfvly4hvkk.png" alt="Investarr Logo">
        </div>
        <div class="content">
            <p>Dear User,</p>
            <p>Thank you for reaching out! At Investarr, we specialize in connecting investors with innovative startups and entrepreneurs with the funding they need to succeed.</p>
            <p>Here are some of the key benefits we offer:</p>
            <ul>
                <li><strong>Exclusive Opportunities:</strong> Gain access to a curated selection of high-potential startups and investment opportunities.</li>
                <li><strong>Expert Guidance:</strong> Receive personalized support and advice from our experienced team to help you make informed investment decisions.</li>
                <li><strong>Networking Events:</strong> Participate in exclusive events and workshops to network with other investors and industry leaders.</li>
                <li><strong>Comprehensive Resources:</strong> Utilize our extensive resources and tools to evaluate and manage your investments effectively.</li>
            </ul>
            <p>Our team will be in touch soon to discuss how we can best support your investment goals.</p>
            <p>In the meantime, feel free to explore our platform and learn more about how we can help you achieve your business objectives.</p>
            <p><a href="https://investarr.com/get-started" class="button">Get Started</a></p>
        </div>
        <div class="footer">
            <p>If you have any questions, please do not hesitate to contact us at support@investarr.com.</p>
            <p>&copy; 2024 Investarr. All rights reserved.</p>
        </div>
    </div>
</body>

</html>
"""


def SignUpEmailTemplate(first_name, last_name):
    return f"""
    <!DOCTYPE html>
    <html>
    
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f7f7f7;
                color: #333;
                padding: 20px;
            }}
    
            p {{
                font-size: 18px;
                line-height: 1.6;
                margin: 10px 0;
            }}
    
            .container {{
                background-color: #ffffff;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                max-width: 600px;
                margin: auto;
            }}
    
            .header {{
                background-color: #483BBF;
                color: #ffffff;
                padding: 25px 0;
                text-align: center;
                border-radius: 10px 10px 0 0;
            }}
    
            .content {{
                margin: 30px 0;
            }}
    
            ul {{
                margin: 10px 0;
                padding-left: 20px;
            }}
    
            li {{
                margin-bottom: 10px;
                font-size: 18px;
            }}
    
            img {{
                max-width: 200px;
                height: auto;
            }}
    
            .button {{
                display: inline-block;
                padding: 10px 20px;
                color: #ffffff;
                background-color: #483BBF;
                text-align: center;
                border-radius: 5px;
                text-decoration: none;
                font-size: 16px;
            }}
    
            .footer {{
                margin-top: 20px;
                font-size: 12px;
                color: #999;
                text-align: center;
            }}
        </style>
    </head>
    
    <body>
        <div class="container">
            <div class="header">
                <img src="https://res.cloudinary.com/dl8ppbbgu/image/upload/v1721162465/nv1w8ek2vgjfvly4hvkk.png" alt="Investarr Logo">
            </div>
            <div class="content">
                <p>Dear user</p>
                <p>Welcome to Investarr! Thank you for signing up and becoming a member of our community.</p>
                <p>Here are some of the benefits you can enjoy:</p>
                <ul>
                    <li><strong>Access to Exclusive Opportunities:</strong> Explore curated startups and investment opportunities.</li>
                    <li><strong>Expert Guidance:</strong> Receive personalized advice to make informed investment decisions.</li>
                    <li><strong>Networking Events:</strong> Connect with other investors and industry leaders.</li>
                    <li><strong>Comprehensive Resources:</strong> Utilize tools to manage your investments effectively.</li>
                </ul>
                <p>We look forward to supporting you on your investment journey. Feel free to explore our platform and discover more about how we can help you achieve your business objectives.</p>
                <p><a href="https://investarr.com/get-started" class="button">Get Started</a></p>
            </div>
            <div class="footer">
                <p>If you have any questions, please do not hesitate to contact us at support@investarr.com.</p>
                <p>&copy; 2024 Investarr. All rights reserved.</p>
            </div>
        </div>
    </body>
    
    </html>
    """



# def ContactUsEmailTemplate(name):
#     return f"""
#     <!DOCTYPE html>
# <html>

# <head>
#     <style>
#         body {{
#             font-family: Arial, sans-serif;
#             background-color: #f7f7f7;
#             color: #333;
#             padding: 20px;
#         }}

#         p {{
#             font-size: 18px;
#             line-height: 1.6;
#             margin: 10px 0;
#         }}

#         .container {{
#             background-color: #ffffff;
#             padding: 20px;
#             border-radius: 10px;
#             box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
#             max-width: 600px;
#             margin: auto;
#         }}

#         .header {{
#             background-color: #483BBF;
#             color: #ffffff;
#             padding: 25px 0;
#             text-align: center;
#             border-radius: 10px 10px 0 0;
#         }}

#         .content {{
#             margin: 30px 0;
#         }}

#         .footer {{
#             margin-top: 20px;
#             font-size: 12px;
#             color: #999;
#             text-align: center;
#         }}
#     </style>
# </head>

# <body>
#     <div class="container">
#         <div class="header">
#             <h1>Contact Us</h1>
#         </div>
#         <div class="content">
#             <p>Dear {name},</p>
#             <p>Thank you for reaching out to us! We appreciate your inquiry and want to assure you that our team is dedicated to responding to your questions and concerns as quickly as possible.</p>
#             <p>Here’s what you can expect:</p>
#             <ul>
#                 <li><strong>Timely Response:</strong> We strive to respond to all inquiries within 24-48 hours.</li>
#                 <li><strong>Personalized Assistance:</strong> Your concerns are important to us, and we will provide you with tailored support.</li>
#                 <li><strong>Ongoing Communication:</strong> We will keep you updated on the status of your inquiry.</li>
#             </ul>
#             <p>If you have any urgent questions, feel free to contact us directly at <a href="mailto:support@investarr.com">support@investarr.com</a>.</p>
#             <p>Thank you for choosing Investarr. We look forward to assisting you!</p>
#         </div>
#         <div class="footer">
#             <p>&copy; 2024 Investarr. All rights reserved.</p>
#         </div>
#     </div>
# </body>

# </html>
# """

def ContactUsEmailTemplate(name):
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            /* Your styles here */
        </style>
    </head>
    <body>
        <h1>Hello, {name}!</h1>
        <p>Thank you for contacting us. We will get back to you shortly!</p>
        <p>Best regards,<br>The Investarr Team</p>
    </body>
    </html>
    """
