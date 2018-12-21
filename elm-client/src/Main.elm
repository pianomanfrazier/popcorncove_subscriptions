module Main exposing (..)


import Browser
import Browser.Navigation as Nav
import Dict
import Html
import Page.Items as Items
import Page.Home as Home
import Skeleton
import Url
import Url.Parser as Parser exposing (Parser, (</>), custom, fragment, map, oneOf, s, top)



-- MAIN


main =
  Browser.application
    { init = init
    , view = view
    , update = update
    , subscriptions = subscriptions
    , onUrlRequest = LinkClicked
    , onUrlChange = UrlChanged
    }



-- MODEL


type alias Model =
  { key : Nav.Key
  , page : Page
  }


type Page
  = Items Items.Model
  | NotFound
  | Home Home.Model



-- SUBSCRIPTIONS


subscriptions : Model -> Sub Msg
subscriptions model =
  Sub.none



-- VIEW


view : Model -> Browser.Document Msg
view model =
  case model.page of
    NotFound ->
      Skeleton.view never
        { title = "Not Found"
        , attrs = []
        , kids = [ Html.div [] [ Html.text "404 Not Found"] ]
        }

    Items items->
      Skeleton.view ItemsMsg (Items.view items)

    Home home ->
      Skeleton.view HomeMsg (Home.view home)



-- INIT


init : () -> Url.Url -> Nav.Key -> ( Model, Cmd Msg )
init _ url key =
  stepUrl url
    { key = key
    , page = Items ( Items.Model 5 )
    }



-- UPDATE


type Msg
  = NoOp
  | LinkClicked Browser.UrlRequest
  | UrlChanged Url.Url
  | ItemsMsg Items.Msg
  | HomeMsg Home.Msg



update : Msg -> Model -> ( Model, Cmd Msg )
update message model =
  case message of
    NoOp ->
      ( model, Cmd.none )

    LinkClicked urlRequest ->
      case urlRequest of
        Browser.Internal url ->
          ( model
          , Nav.pushUrl model.key (Url.toString url)
          )

        Browser.External href ->
          ( model
          , Nav.load href
          )

    UrlChanged url ->
      stepUrl url model

    ItemsMsg msg ->
      case model.page of
        Items items -> stepItems model (Items.update msg items)
        _             -> ( model, Cmd.none )

    HomeMsg msg ->
      case model.page of
        Home home -> stepHome model (Home.update msg home)
        _         -> ( model, Cmd.none )



stepItems : Model -> ( Items.Model, Cmd Items.Msg ) -> ( Model, Cmd Msg )
stepItems model (items, cmds) =
  ( { model | page = Items items }
  , Cmd.map ItemsMsg cmds
  )


stepHome : Model -> ( Home.Model, Cmd Home.Msg ) -> ( Model, Cmd Msg )
stepHome model (home, cmds) =
  ( { model | page = Home home}
  , Cmd.map HomeMsg cmds
  )


-- ROUTER


stepUrl : Url.Url -> Model -> (Model, Cmd Msg)
stepUrl url model =
  let
    parser =
      oneOf
        [ route top
          ( stepHome model (Home.init 7) )
        , route ( s "items" )
          ( stepItems model (Items.init 8) )
        ]
  in
  case Parser.parse parser url of
    Just answer ->
      answer

    Nothing ->
      ( { model | page = NotFound }
      , Cmd.none
      )


route : Parser a b -> a -> Parser (b -> c) c
route parser handler =
  Parser.map handler parser
