library(bslib)
library(shiny)


#' importFrom shiny fluidPage, textOutput
#' importFrom layout_sidebar, bs_theme, page_fluid
library(bslib)
library(shiny)

button_ui <- bslib::page_fluid(
  # title bar displays name of game
  title = txt_start[1],

  # set theme
  theme = bslib::bs_theme(
    preset = "superhero",
    base_font = "courier",
    heading_font = "courier",
    font_scale = 3
  ),

  # display text
  bslib::card(
    full_screen = TRUE,
    sidebar = sidebar(
      bslib::card(
        title = "Job Title",
        p("Data Scientist")
      )
    ),
    bslib::card(
      
      # preamble
      shiny::textOutput("preamble_txt"),
      tags$img(src = "trash-solid.svg", height = "500px", width = "500px")
    )
  )

  # display progress plot - todo

  # display button
)

# server 
button_server <- function(input, output, session) {
  # use this to configure bs_theme in ui  
  # bslib::bs_themer()

  # render text
  output$preamble_txt <- shiny::renderText({
    txt_start[2]
  })


  # render progress plot - todo 
}

shinyApp(ui = button_ui, server = button_server)