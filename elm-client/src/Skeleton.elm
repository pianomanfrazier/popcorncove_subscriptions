module Skeleton exposing
    ( Details
    , view
    )

import Browser
import Css
import Html
import Html.Styled as HS exposing (..)
import Html.Styled.Attributes as HSA exposing (..)
import Html.Styled.Lazy exposing (..)
import Json.Decode as D



-- NODE


type alias Details msg =
    { title : String
    , attrs : List (HS.Attribute msg)
    , kids : List (HS.Html msg)
    }



-- VIEW


view : (a -> msg) -> Details a -> Browser.Document msg
view toMsg details =
    let
        body =
            div details.attrs details.kids
    in
    { title =
        details.title
    , body =
            [ HS.toUnstyled viewHeader
            , Html.map toMsg <| HS.toUnstyled body
            , HS.toUnstyled viewFooter
            ]
    }



-- VIEW HEADER


viewHeader : Html msg
viewHeader =
    div []
        [ a [ href "/" ] [ text "Home" ]
        , a [ href "/items" ] [ text "Add Subscription Items" ]
        ]



-- VIEW FOOTER


viewFooter : Html msg
viewFooter =
    div [] [ text " ~~~ FOOTER ~~~ " ]
