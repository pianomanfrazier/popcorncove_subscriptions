module Page.Items exposing
    ( Model
    , Msg
    , init
    , update
    , view
    )

import Html exposing (..)
import Skeleton



-- Model


type alias Model =
    { num : Int }


init : Int -> ( Model, Cmd Msg )
init num =
    ( Model num, Cmd.none )



-- UPDATE


type Msg
    = NoOp


update : Msg -> Model -> ( Model, Cmd msg )
update msg model =
    case msg of
        NoOp ->
            ( model
            , Cmd.none
            )



-- VIEW


view : Model -> Skeleton.Details Msg
view model =
    { title = "Add Subscription Items"
    , attrs = []
    , kids =
        [ div []
            [ h1 [] [text "Subscription Items"]
            ]
        ]
    }
