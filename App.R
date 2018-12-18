library(shiny)
library(rjson)

Sys.setlocale("LC_TIME", "English")

options(shiny.maxRequestSize=4000*1024^2)

ui <- fluidPage(
  
  sidebarLayout(
    
    sidebarPanel(
      fileInput("json_file", "Choose Json File",
                multiple = FALSE,
                accept = c("application/json",
                           "text/comma-separated-values,text/plain",
                           ".json")),
      checkboxGroupInput("tweet", label = NULL, 
                         choices = list("Tweets" = 1, "Retweets" = 2),
                         selected = 1),
      dateRangeInput("dates", label = NULL, start = "2008-01-01", end = "2018-12-31"),
      textInput("textName", label = NULL, value = "Company Name..."),
      textInput("textWord", label = NULL, value = "Search..."),
      div(style="display: inline-block;vertical-align:top; width: 85px;",actionButton("analyze", label = "Analyze")),
      div(style="display: inline-block;vertical-align:top; width: 85px;",downloadButton("downloadData", "Download"))
    ),
    
    mainPanel(
    
      
    )
  )
)

server <- function(input, output) {
  
  observeEvent(input$analyze, {
    
    inFile <- input$json_file
    
    json_data <- fromJSON(paste(readLines(inFile), collapse=""))
    
    #Vectors
    tweets <- c()
    r <- c()
    rt <- c()
    fav <- c()
    date <- c()
    name <- c()
    
    inc <- TRUE
    unclean_tweet <- ""

    for (i in 1:length(json_data)) {
      
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
            
            unclean_tweet <- json_data[[i]][['retweeted_status']][['extended_tweet']][['full_text']]
            
            
          } else if (!is.null('text' %in% json_data[[i]][['retweeted_status']])) {
              
              unclean_tweet <- json_data[[i]][['retweeted_status']][['text']]
              
          }
        }
      }
      
      if (!unclean_tweet == "") {
        
        clean_tweet = gsub("&amp", "", unclean_tweet)
        clean_tweet = gsub("(RT|via)((?:\\b\\W*@\\w+)+)", "", clean_tweet)
        clean_tweet = gsub("@\\w+", "", clean_tweet)
        clean_tweet = gsub("[[:punct:]]", "", clean_tweet)
        clean_tweet = gsub("[[:digit:]]", "", clean_tweet)
        clean_tweet = gsub("http\\w+", "", clean_tweet)
        clean_tweet = gsub("[ \t]{2,}", "", clean_tweet)
        clean_tweet = gsub("^\\s+|\\s+$", "", clean_tweet) 
        clean_tweet = gsub("#\\w+", "", clean_tweet)
      
        if (!input$textName == "Company Name...") {
          if (!input$textName %in% json_data[[i]][['user']][['name']]) {
            inc <- FALSE 
          } else if (!input$textWord == "Search...") {
            if (!input$textWord %in% clean_tweet) {
              inc <- FALSE
            }
          }
        } else if (!input$textWord == "Search...") {
          if (!input$textWord %in% clean_tweet) {
            inc <- FALSE
          }
        }
        
        if (input$dates[[1]] <=  as.Date(json_data[[i]][['created_at']], format = "%a %b %d %H:%M:%S +0000 %Y") &&  as.Date(json_data[[i]][['created_at']], format = "%a %b %d %H:%M:%S +0000 %Y") <= input$dates[[2]]) {
          inc <- FALSE
        }
        
        if (inc){
          
          tweets <- c(tweets, clean_tweet)
          name <- c(name, json_data[[i]][['user']][['name']])
          date <- c(date, as.POSIXct(json_data[[i]][['created_at']], format = "%a %b %d %H:%M:%S +0000 %Y"))
          rt <- c(rt, json_data[[i]][['retweet_count']])
          r <- c(r, json_data[[i]][['reply_count']])
          fav <- c(fav, json_data[[i]][['favorite_count']])
        }
      }
      
      unclean_tweet <- ""
    }
    
    #Create DataFrame
    df = data.frame(name, date, tweet, rt, r, fav)
    
      
  })
  
  output$downloadData <- downloadHandler(
    filename = function() {
      paste("Data - ", Sys.Date(), ".csv", sep = "")
    },
    content = function(file) {
      write.csv(df, file)
    }
  )
  
}

shinyApp(ui = ui, server = server)