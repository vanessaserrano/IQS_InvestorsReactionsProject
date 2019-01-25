library(shiny)
library(rjson)
library(tm)
library(wordcloud)
library(RColorBrewer)
library(RPostgreSQL)
library(RODBC)


Sys.setlocale("LC_TIME", "English")
options(shiny.maxRequestSize = 4000 * 1024 ^ 2)

json_data <- ""
df <- NULL
dfWC <- NULL
cleanWordcloud <- "No se han cargado datos"
cn <- NULL

#Render Analyze UI
renderParameters <- function() {
  ui <- renderUI({
    tagList(
      checkboxGroupInput(
        "tweet",
        label = NULL,
        choices = list("Tweets" = 1, "Retweets" = 2),
        selected = 1
      ),
      dateRangeInput(
        "dates",
        label = NULL,
        start = "2008-01-01",
        end = "2018-12-31"
      ),
      selectInput(
        "compSel",
        label = NULL,
        choices = NULL,
        selected = NULL,
        multiple = TRUE
      ),
      textInput("textWord", label = NULL, value = "Search..."),
      div(style = "display: inline-block;vertical-align:top; width: 85px;", actionButton("analyze", label = "Analyze")),
      div(style = "display: inline-block;vertical-align:top; width: 250px;", downloadButton("downloadData", "Download"))
    )
  })
  return(ui)
}

server <- function(input, output, session) {
  output$status <- renderText({
    "Ready!"
  })
  
  #Uploads and Connections
  
  #Json file
  observeEvent(input$json_file, {
    tryCatch({
      json_data <<- fromJSON(file = input$json_file[["datapath"]])
      companies <- c()
      for (i in 1:length(json_data)) {
        if (!json_data[[i]][['user']][['name']] %in% companies) {
          companies <- c(companies, json_data[[i]][['user']][['name']])
        }
      }
      updateSelectInput(
        session,
        inputId = "compSel",
        label = NULL,
        choices = companies,
        selected = NULL
      )
      
      output$param <- renderParameters()
      
      output$status <- renderText({
        "Data Uploaded!"
      })
      
    },
    error = function(e) {
      print(e)
      output$status <- renderText({
        "Could not upload the data!"
      })
    })
  })
  
  #Access file
  observeEvent(input$access_file, {
    tryCatch({
      odbcDriverConnect(
        "Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\\Users\\daWigs\\Documents\\Project Database.accdb"
      )
      
      output$param <- renderParameters()
      
      output$status <- renderText({
        "Data Uploaded!"
      })
    },
    error = function(e) {
      output$status <- renderText({
        "Could not upload the data!"
      })
      
    })
  })
  
  #Server connection
  observeEvent(input$cnn, {
    drv <- dbDriver("PostgreSQL")
    
    tryCatch({
      cn <<- dbConnect(
        drv,
        dbname   = input$dbName,
        user = input$user,
        password = input$pass,
        host     = input$host,
        port     =  	strtoi(input$port)
      )
      
      output$param <- renderParameters()
      
      output$status <- renderText({
        "Connection Successful!"
      })
    },
    error = function(e) {
      output$status <- renderText({
        "Connection Failed!"
      })
    })
    
  })
  #End
  
  #Analyze
  observeEvent(input$analyze, {
    #Json Analyze
    if (input$dwnSel[[1]] == 1) {
      tweets <- c()
      r <- c()
      rt <- c()
      fav <- c()
      date <- c()
      name <- c()
      
      unclean_tweet <- ""
      
      
      for (i in 1:length(json_data)) {
        if ((
          input$dates[[1]] <=  as.Date(json_data[[i]][['created_at']], format = "%a %b %d %H:%M:%S +0000 %Y") &&
          as.Date(json_data[[i]][['created_at']], format = "%a %b %d %H:%M:%S +0000 %Y") <= input$dates[[2]]
        )) {
          if (is.null(input$compSel) ||
              json_data[[i]][['user']][['name']] %in% input$compSel) {
            if (1 %in% input$tweet) {
              if (is.null(json_data[[i]][['retweeted_status']])) {
                if (!is.null(json_data[[i]][['extended_tweet']])) {
                  if (!'RT' %in% json_data[[i]][['extended_tweet']][['full_text']]) {
                    unclean_tweet <- json_data[[i]][['extended_tweet']][['full_text']]
                  }
                  
                } else if (!is.null('text' %in% json_data[[i]])) {
                  if (!'RT' %in% json_data[[i]][['extended_tweet']][['full_text']]) {
                    unclean_tweet <- json_data[[i]][['text']]
                    
                  }
                }
              }
            } else if (2 %in% input$tweet) {
              if (!is.null(json_data[[i]][['retweeted_status']])) {
                if (!is.null(json_data[[i]][['retweeted_status']][['extended_tweet']])) {
                  unclean_tweet <-
                    json_data[[i]][['retweeted_status']][['extended_tweet']][['full_text']]
                  
                  
                } else if (!is.null('text' %in% json_data[[i]][['retweeted_status']])) {
                  unclean_tweet <- json_data[[i]][['retweeted_status']][['text']]
                  
                }
              }
            }
            
            words <- strsplit(input$textWord, split = ",")
            if (input$textWord == "Search..." ||
                words %in% unclean_tweet) {
              clean_tweet = gsub("&amp", "", unclean_tweet)
              clean_tweet = gsub("(RT|via)((?:\\b\\W*@\\w+)+)", "", clean_tweet)
              clean_tweet = gsub("@\\w+", "", clean_tweet)
              clean_tweet = gsub("[[:punct:]]", "", clean_tweet)
              clean_tweet = gsub("[[:digit:]]", "", clean_tweet)
              clean_tweet = gsub("http\\w+", "", clean_tweet)
              clean_tweet = gsub("[ \t]{2,}", "", clean_tweet)
              clean_tweet = gsub("^\\s+|\\s+$", "", clean_tweet)
              clean_tweet = gsub("#\\w+", "", clean_tweet)
              
              tweets <- c(tweets, clean_tweet)
              name <- c(name, json_data[[i]][['user']][['name']])
              date <-
                c(date, format(
                  as.Date(json_data[[i]][['created_at']], format = "%a %b %d %H:%M:%S +0000 %Y"),
                  format = "%d-%m-%Y"
                ))
              rt <- c(rt, json_data[[i]][['retweet_count']])
              r <- c(r, json_data[[i]][['reply_count']])
              fav <- c(fav, json_data[[i]][['favorite_count']])
            }
          }
        }
      }
      df <<- data.frame(name, date, tweets, rt, r, fav)
      updateSelectInput(
        session,
        inputId = "compSelWC",
        label = NULL,
        choices = unique(df$name),
        selected = NULL
      )
      output$status <- renderText({
        "Data Analyzed! Ready to Download"
      })
    }
    #Server Analyze
    if (input$dwnSel) {
      
    }
  })
  
  observeEvent(input$compSelWC, {
    if (!is.null(input$compSelWC)) {
      dfWC <<- df[[input$compSelWC %in% df$name]]
    }
    
    wordcloudText <- paste(df$tweets, collapse = " ")
    
    cleanWordcloud <<- Corpus(VectorSource(wordcloudText))
    cleanWordcloud <<- tm_map(cleanWordcloud, stripWhitespace)
    cleanWordcloud <<- tm_map(cleanWordcloud, tolower)
    cleanWordcloud <<- tm_map(cleanWordcloud, removeNumbers)
    cleanWordcloud <<- tm_map(cleanWordcloud, removePunctuation)
    cleanWordcloud <<-
      tm_map(cleanWordcloud, removeWords, stopwords("english"))
    cleanWordcloud <<-
      tm_map(
        cleanWordcloud,
        removeWords,
        c(
          "and",
          "the",
          "our",
          "that",
          "for",
          "are",
          "also",
          "more",
          "has",
          "must",
          "have",
          "should",
          "this",
          "with"
        )
      )
    
  })
  
  observeEvent(input$datesWC, {
    if (!is.null(df)) {
      dfWC <<-
        df[[input$datesWC[[1]] <= df$date &&
              df$date <= input$datesWC[[2]]]]
      
      wordcloudText <- paste(df$tweets, collapse = " ")
      
      cleanWordcloud <<- Corpus(VectorSource(wordcloudText))
      cleanWordcloud <<- tm_map(cleanWordcloud, stripWhitespace)
      cleanWordcloud <<- tm_map(cleanWordcloud, tolower)
      cleanWordcloud <<- tm_map(cleanWordcloud, removeNumbers)
      cleanWordcloud <<- tm_map(cleanWordcloud, removePunctuation)
      cleanWordcloud <<-
        tm_map(cleanWordcloud, removeWords, stopwords("english"))
      cleanWordcloud <<-
        tm_map(
          cleanWordcloud,
          removeWords,
          c(
            "and",
            "the",
            "our",
            "that",
            "for",
            "are",
            "also",
            "more",
            "has",
            "must",
            "have",
            "should",
            "this",
            "with"
          )
        )
    }
  })
  
  
  wordcloud_rep <- repeatable(wordcloud)
  
  output$wcPlot <-
    renderPlot({
      wordcloud_rep(
        cleanWordcloud,
        scale = c(4, 0.5),
        min.freq = input$freq,
        max.words = input$max,
        colors = brewer.pal(8, "Dark2")
      )
    })
  
}
