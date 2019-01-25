library(shiny)

ui <- fluidPage(

  tabsetPanel(
    id = "tabs",
    tabPanel("Analyze",
             sidebarLayout(
               sidebarPanel(
                 selectInput("dwnSel", label = NULL, choices = list("Json", "Amazon AWS", "MS Access"), selected = "Amazon AWS"),
                 conditionalPanel(condition = "input.dwnSel == 'Json'",
                                  fileInput("json_file", "Choose Json File", multiple = FALSE, accept = c("application/json", "text/comma-separated-values,text/plain", ".json"))
                 ),
                 conditionalPanel(condition = "input.dwnSel == 'Amazon AWS'",
                                  textInput("host", label = "Host", value = "mydbproject.cnz4uq4r9hue.eu-west-3.rds.amazonaws.com"),
                                  textInput("port", label = "Port", value = "5432"),
                                  textInput("dbName", label = "Database name", value = "dbproject"),
                                  textInput("user", label = "Username", value = "username"),
                                  passwordInput("pass", label = "Password", value = "password"),
                                  actionButton("cnn", label = "Connect")
                                  
                 ),
                 conditionalPanel(condition = "input.dwnSel == 'MS Access'",
                                  fileInput("access_file", "Choose Access File", multiple = FALSE, accept = c(".accdb",".mdb"))
                 ),
                 uiOutput("param"),
                 h3(),
                 textOutput("status")
               ),
               mainPanel()
             )
    ),
    tabPanel("Wordcloud",
             sidebarLayout(
                sidebarPanel(
                  selectInput("compSelWC", label = NULL, choices = NULL, selected = NULL, multiple = TRUE),
                  dateRangeInput("datesWC", label = NULL, start = "2008-01-01", end = "2018-12-31"),
                  sliderInput("freq", "Minimum Frequency:", min = 1,  max = 50, value = 1),
                  sliderInput("max", "Maximum Number of Words:", min = 1,  max = 300,  value = 1)
                ),
                mainPanel(plotOutput("wcPlot"))
              )
    )
  )
)

