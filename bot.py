from telegram.ext import Updater, CommandHandler, RegexHandler, MessageHandler,Filters
from telegram import ReplyKeyboardMarkup,Bot
import telegram.ext
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters,PollAnswerHandler, ConversationHandler,CallbackQueryHandler
from telegram import KeyboardButton
from telegram.error import TelegramError
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
import requests,json
import os
import requests
import json
import random
import paytmchecksum
from captcha.image import ImageCaptcha
import string
BAS,DAD,FI,FA,FS,FB,FC,BAG,HAM,AB,HA,HB= range(12)
TOKEN = "1486301742:AAFVT-UxjwuJONMKDK7rAtC9nwVRPafBVUI"
refr = [0.1]
dci=[0.1]
wmin=[1.0]
wmax=[100]
qa=[0.1]
data = []
dash_key = [['🎁 Daily Checkin'],['📘 Daily Quiz','💰 Balance' ],['💵 Withdrawl'],['👫 Refer And Earn']]
admin_key = [['👥 Users','📝 Get List'],['👫 Upadte Refferal Amount'],['🎁 Upadte Checkin Amount'],['📘 Update Quiz','💰 Update Quiz Amount'],['💵 Upadte Withdrawal Amount']]
q=["How many eggs do you need for a cake?"]
questions = ["1", "2", "4", "20"]
qc=[0]
def start(update, context):
    user = str(update.effective_user.id)
    data = json.load(open('users.json','r'))
    if update.message.chat.type == 'private':
        if user=="820087402":
            reply_markup = ReplyKeyboardMarkup(admin_key,resize_keyboard=True)
            update.message.reply_text("Welcome to Admin Dashboard",reply_markup=reply_markup)
            return DAD
        else:
            if user not in data['users']:
                data['users'].append(user)
                if user not in data['checkin']:
                    data['checkin'][user] = "0"
                if user not in data['DailyQuiz']:
                    data['DailyQuiz'][user] = "0"
                if user not in data['withd']:
                    data['withd'][user] = "0"
                if len(ref_id) > 1:
                    data['referred'][ref_id[1]] += refr[0]              
                data['total'] += 1
                data['id'][user] = data['total']
                data['referred'][data['total']] = 0
                json.dump(data,open('users.json','w'))
                reply_markup = ReplyKeyboardMarkup(dash_key,resize_keyboard=True)
                update.message.reply_text("🎁 Welcome to our bot \n\n""🔸️Daily Checkin\n\n""🔸️Complete Quiz and Earn\n\n""🔸️Refer And Earn\n\n""🔸️Instant Payment\n\n""🔸️https://t.me/joinchat/AAAAAEMZsQF0vRUMfO8i1Q",disable_web_page_preview=True,reply_markup=reply_markup)
                return BAS                
            else:
                reply_markup = ReplyKeyboardMarkup(dash_key,resize_keyboard=True)
                update.message.reply_text("🎁 Welcome to our bot \n\n""🔸️Daily Checkin\n\n""🔸️Complete Quiz and Earn\n\n""🔸️Refer And Earn\n\n""🔸️Instant Payment\n\n""🔸️https://t.me/joinchat/AAAAAEMZsQF0vRUMfO8i1Q", disable_web_page_preview=True,reply_markup=reply_markup)
                return BAS
    else:
        msg = '{} \n. I don\'t reply in group, come in private'.format(config['intro'])
        update.message.reply_text(msg)

def dad(update, context):
    user = str(update.effective_user.id)
    c=update.message.text
    data = json.load(open('users.json','r'))
    if c=="👥 Users":
        msg = "A total of {} have joined this program".format(data['total']-1000)
        reply_markup = ReplyKeyboardMarkup(admin_key,resize_keyboard=True)
        update.message.reply_text(msg,reply_markup=reply_markup)
        return DAD
    elif c=="📝 Get List":
        f = open('users.csv','w')
        f.write("Telegram Id,Balance\n")
        for u in data['users']:
            i = str(data['id'][u])
            refrrd = data['referred'][i]
            d = "{},{}\n".format(u,refrrd)
            f.write(d)
        f.close()
        bot = Bot(TOKEN)
        reply_markup = ReplyKeyboardMarkup(admin_key,resize_keyboard=True)
        bot.send_document(chat_id=update.message.chat.id, document=open('users.csv','rb'),reply_markup=reply_markup)
        return DAD
    elif c=="👫 Upadte Refferal Amount":
        context.bot.send_message(chat_id=update.effective_user.id,text="Please Send the  Referal Amount.")
        return FI

    elif c=="💰 Update Quiz Amount":
        context.bot.send_message(chat_id=update.effective_user.id,text="Please Send the  Quiz Amount.")
        return HA
    elif c=="💵 Upadte Withdrawal Amount":
        context.bot.send_message(chat_id=update.effective_user.id,text="Please Send the  withdrawl max and min Amount seperated by ',' (min,max) only in digits")
        return HB
    
    elif c=="🎁 Upadte Checkin Amount":
        context.bot.send_message(chat_id=update.effective_user.id,text="Please Send the  Checkin Amount.")
        return FA
    elif c=="📘 Update Quiz":
        context.bot.send_message(chat_id=update.effective_user.id,text="Please Send the Quiz Question.")
        return FS
def fs(update, context):
   msg=update.message.text
   q.pop(0)
   q.append(msg)
   context.bot.send_message(chat_id=update.effective_user.id,text="Please Send the options seperated by ',' .")
   return FB
def fb(update, context):
    msg=update.message.text
    d=msg.split(",")
    questions.clear()
    for names in d:
        questions.append(names)
    context.bot.send_message(chat_id=update.effective_user.id,text="send the correct option in digit 0 or 1 or 2...")
    return FC
def fc(update, context):
    msg=update.message.text
    try:
        msg=int(msg)
        qc.pop(0)
        qc.append(msg)
        reply_markup = ReplyKeyboardMarkup(admin_key,resize_keyboard=True)
        context.bot.send_message(chat_id=update.effective_user.id,text="Quiz updated Successfully",reply_markup=reply_markup)
        return BAS
    except:
      context.bot.send_message(chat_id=update.effective_user.id,text="Invalid ID send again only in digit")
      return FC
def ha(update, context):
    try:
        c=update.message.text
        c=float(c)
        qa.pop(0)
        qa.append(c)
        reply_markup = ReplyKeyboardMarkup(admin_key,resize_keyboard=True)
        update.message.reply_text("Amount upadted successfully.",reply_markup=reply_markup)
        return DAD
    except:
        context.bot.send_message(chat_id=update.effective_user.id,text="Invalid Amount! please send amount only in digits")
        return HA
def hb(update, context):
    try:
        c=update.message.text.split(",")
        cmin=float(c[0])
        cmax=float(c[1])
        wmin.pop(0)
        wmax.pop(0)
        wmin.append(cmin)
        wmax.append(cmax)
        reply_markup = ReplyKeyboardMarkup(admin_key,resize_keyboard=True)
        update.message.reply_text("Amount upadted successfully.",reply_markup=reply_markup)
        return DAD
    except:
        context.bot.send_message(chat_id=update.effective_user.id,text="Invalid Amount! please send amount only in digits")
        return HA
    
def fi(update, context):
    user = str(update.effective_user.id)
    try:
        c=update.message.text
        c=float(c)
        refr.pop(0)
        refr.append(c)
        reply_markup = ReplyKeyboardMarkup(admin_key,resize_keyboard=True)
        update.message.reply_text("Amount upadted successfully.",reply_markup=reply_markup)
        return DAD
    except:
        context.bot.send_message(chat_id=update.effective_user.id,text="Invalid Amount! please send amount only in digits")
        return FI


def fa(update, context):
    try:
        user = str(update.effective_user.id)
        c=update.message.text
        c=float(c)
        dci.pop(0)
        dci.append(c)
        reply_markup = ReplyKeyboardMarkup(admin_key,resize_keyboard=True)
        update.message.reply_text("Amount upadted successfully.",reply_markup=reply_markup)
        return DAD
    except:
        context.bot.send_message(chat_id=update.effective_user.id,text="Invalid Amount! please send amount only in digits")
        return FA

def bas(update, context):
    user = str(update.effective_user.id)
    c=update.message.text
    data = json.load(open('users.json','r'))
    if c=="🎁 Daily Checkin":
        v=data['checkin'][user] 
        if v=="0":   
          i = str(data["id"][user])
          data['referred'][i] += dci[0]         
          reply_markup = ReplyKeyboardMarkup(dash_key,resize_keyboard=True)
          update.message.reply_text("Today Reward - Rs. {}\n\n""Daily Bonus Program You can receive bonus every 24 hours".format(str(dci[0])),reply_markup=reply_markup)
          data['checkin'][user] = "1"
          context.job_queue.run_once(callback_minute, 86400,context=user)
          json.dump(data,open('users.json','w'))
          return BAS
        else:
          reply_markup = ReplyKeyboardMarkup(dash_key,resize_keyboard=True)
          update.message.reply_text("❌ Sorry ,you have received your Bonus today",reply_markup=reply_markup)
          return BAS
    elif c=="💰 Balance":
        i = str(data["id"][user])
        reply_markup = ReplyKeyboardMarkup(dash_key,resize_keyboard=True)
        update.message.reply_text("💥 Welcome To Your Wallet\n\n""Here u will know all about ur earning details in this bot\n\n""💵 Account Balance : Rs. {}\n\n""Click Withdraw to Transfer Paytm".format(data['referred'][i]),reply_markup=reply_markup)
        return BAS
    elif c=="👫 Refer And Earn":
        reply_markup = ReplyKeyboardMarkup(dash_key,resize_keyboard=True)
        user = str(update.effective_user.id)
        msg = 'https://t.me/Cashwala_bot?start={}'.format(data['id'][user])
        update.message.reply_text("🙋‍♂ Hello\n\n""Here u will get ur Referral Link which u can share to Your Friends and start Earning Unlimited Paytm cash\n\n""Link - {}".format(msg),reply_markup=reply_markup)
        return BAS
    elif c=="📘 Daily Quiz":
        vb=data['DailyQuiz'][user] 
        if vb=="0":
            context.bot.send_poll(chat_id=update.effective_user.id,question=q[0], options=questions,is_anonymous=False,type="quiz",allows_multiple_answers=False, explanation="Wrong option come back after 24h.",correct_option_id=qc[0])
            return BAS
        else:
          reply_markup = ReplyKeyboardMarkup(dash_key,resize_keyboard=True)
          update.message.reply_text("Sorry ,you have Done your today Quiz",reply_markup=reply_markup)
          return BAS
    elif c=="💵 Withdrawl":
        i = str(data["id"][user])
        am=data['referred'][i]
        cx=data['withd'][user]
        if cx=="0":
            am=int(am)
            if am>=wmin[0]:
                context.bot.send_message(chat_id=update.effective_user.id,text="Please Send amount that You want to Withdraw send only in digits")
                return BAG
            else:
                reply_markup = ReplyKeyboardMarkup(dash_key,resize_keyboard=True)
                update.message.reply_text("Your Balance is less than Minimum Withdrawl amount {}".format(str(wmin[0])),reply_markup=reply_markup)
                return BAS
        else:
            reply_markup = ReplyKeyboardMarkup(dash_key,resize_keyboard=True)
            update.message.reply_text("you can only withdraw once day. Please come back after 24h.",reply_markup=reply_markup)
            return BAS


def bag(update, context):
    msg=update.message.text
    user = str(update.effective_user.id)
    data = json.load(open('users.json','r'))
    try:
        msg=int(msg)
        i = str(data["id"][user])
        am=data['referred'][i]
        am=int(am)
        global cvb
        cvb=msg
        if msg > am:
            context.bot.send_message(chat_id=update.effective_user.id,text="Amount Exceed your available Balance please send again less amount")
            return BAG
        elif msg < wmin[0]:
            context.bot.send_message(chat_id=update.effective_user.id,text="Minimum withdrawal amount is {}".format(str(wmin[0])))
            return BAG
        elif msg > wmax[0]:
            context.bot.send_message(chat_id=update.effective_user.id,text="Maximum withdrawal amount is {}".format(str(wmax[0])))
            return BAG
        else:
            context.bot.send_message(chat_id=update.effective_user.id,text="Send your paytm Number you will recieve payment on that paytm wallet.")
            return HAM
    except:
    
        context.bot.send_message(chat_id=update.effective_user.id,text="Invalid Amount! Send only in digits again")
        return BAG

def ham(update, context):
    user = str(update.effective_user.id)
    data = json.load(open('users.json','r'))
    try:
        msg=update.message.text
        paytmParams = dict()
        orderID="20201224130531688029"
        amb=float(cvb)
        amb=str(amb)
        number = str(random.randint(0000,9999))
        orderID+=number
        paytmParams["subwalletGuid"]      = "242f7e06-c860-4a14-8eba-5b6d18c4e6e2"
        paytmParams["orderId"]            = orderID
        paytmParams["beneficiaryPhoneNo"] = msg
        paytmParams["amount"]             = amb
        post_data = json.dumps(paytmParams)
        checksum = paytmchecksum.generateSignature(post_data, "cX2gDSq!&ajo4kgN")
        x_mid      = "KJTRIC10516333500679"
        x_checksum = checksum
        url = "https://dashboard.paytm.com/bpay/api/v1/disburse/order/wallet/gratification"
        response = requests.post(url, data = post_data, headers = {"Content-type": "application/json", "x-mid": x_mid, "x-checksum": x_checksum}).json()
        asd=response['status']
        if asd=="ACCEPTED":
            i = str(data["id"][user])
            am=data['referred'][i]
            am=int(am)
            fg=am-cvb
            fg=str(fg)
            data['referred'][i]=fg
            data['withd'][user] = "1"
            json.dump(data,open('users.json','w'))
            reply_markup = ReplyKeyboardMarkup(dash_key,resize_keyboard=True)
            update.message.reply_text("Withdrawl initiated successfully!",reply_markup=reply_markup)
            context.job_queue.run_once(callb, 86400,context=user)
            return BAS
        else:
            reply_markup = ReplyKeyboardMarkup(dash_key,resize_keyboard=True)
            update.message.reply_text("Something Goes wrong please check your wallet is correct and then come back later.",reply_markup=reply_markup)
            return BAS
            
    except:
        reply_markup = ReplyKeyboardMarkup(dash_key,resize_keyboard=True)
        update.message.reply_text("Something Goes wrong please come back later.",reply_markup=reply_markup)
        return BAS


def get_answer(update,context):
  data = json.load(open('users.json','r'))
  user=str(update.poll_answer.user.id)
  ans=int(update.poll_answer.option_ids[0])
  if ans==qc[0]:
    i = str(data["id"][user])
    x = qa[0]
    data['referred'][i] += x
    reply_markup = ReplyKeyboardMarkup(dash_key,resize_keyboard=True)
    context.bot.send_message(chat_id=update.effective_user.id,text="Congrulations you earn RS. {}".format(str(x)),reply_markup=reply_markup)
    data['DailyQuiz'][user]  = "1"
    context.job_queue.run_once(callback_minut, 86400,context=user)
    json.dump(data,open('users.json','w'))
    return BAS
  else:
    data['DailyQuiz'][user]  = "1"
    context.job_queue.run_once(callback_minut, 86400,context=user)
    json.dump(data,open('users.json','w'))
    reply_markup = ReplyKeyboardMarkup(dash_key,resize_keyboard=True)
    context.bot.send_message(chat_id=update.effective_user.id,text="Sorry! come back after 24h.",reply_markup=reply_markup)
    return BAS


def callback_minut(context: telegram.ext.CallbackContext):
    data = json.load(open('users.json','r'))
    job = context.job
    user=job.context
    data['DailyQuiz'][user] = "0"
    json.dump(data,open('users.json','w'))

def callb(context: telegram.ext.CallbackContext):
    data = json.load(open('users.json','r'))
    job = context.job
    user=job.context
    data['withd'][user] = "0"
    json.dump(data,open('users.json','w'))

def callback_minute(context: telegram.ext.CallbackContext):
    data = json.load(open('users.json','r'))
    job = context.job
    user=job.context
    data['checkin'][user] = "0"
    json.dump(data,open('users.json','w'))

def cancel(update, context):
    user = update.message.from_user
    return ConversationHandler.END

if __name__ == '__main__':
    data = json.load(open('users.json','r'))
    updater = Updater(TOKEN,use_context=True)
    dp = updater.dispatcher
    dp.add_handler(PollAnswerHandler(get_answer))
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            FI: [MessageHandler(Filters.text, fi)],
            FA: [MessageHandler(Filters.text, fa)],
            FS: [MessageHandler(Filters.text, fs)],
            FB: [MessageHandler(Filters.text, fb)],
            FC: [MessageHandler(Filters.text, fc)],
            AB: [MessageHandler(Filters.text, ab)],
            BAG: [MessageHandler(Filters.text, bag)],
            HA: [MessageHandler(Filters.text, ha)],
            HB: [MessageHandler(Filters.text, hb)],
            HAM: [MessageHandler(Filters.text, ham)],
            BAS: [MessageHandler(Filters.regex('^(🎁 Daily Checkin|📘 Daily Quiz|💵 Withdrawl|💰 Balance|👫 Refer And Earn)$'), bas)],
            DAD: [MessageHandler(Filters.regex('^(👥 Users|📝 Get List|👫 Upadte Refferal Amount|🎁 Upadte Checkin Amount|💰 Update Quiz Amount|📘 Update Quiz|💵 Upadte Withdrawal Amount)$'), dad)],

        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    dp.add_handler(conv_handler) 
    updater.start_polling()
    updater.idle()
