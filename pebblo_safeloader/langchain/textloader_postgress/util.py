from hashlib import sha256
from typing import Any, Optional


def get_data(
    metadata=False, ids=False, metadatas=False
) -> tuple[
    list[str],
    Optional[dict[str, Any]],
    Optional[list[dict[str, Any]]],
    list[str],
]:
    """
    Get data for PebbloTextLoader

    Args:
        metadata: Include metadata for all texts.
            Optional. Defaults to False.
        ids: Include unique ids for each text.
            Optional. Defaults to False.
        metadatas: Include metadata for each text.
            Optional. Defaults to False.

    Returns:
        tuple: A tuple containing texts, metadata, metadatas, and ids.
    """

    texts = [
        "Wipros board on Friday, January 12 announced an interim dividend of Re 1 per equity share of the face value of Rs 2 each, i.e., a 50 per cent payout for the current financial year along with financial results for the October-December period of the company for the financial year ending March 2024.",
        "Roberts reminded the board of the scheduled retreat coming up in three months, and provided a drafted retreat schedule. The board provided feedback on the agenda and the consensus was that, outside of making a few minor changes, the committee should move forward as planned. No board action required.",
        "Claims: An adaptive pacing system for implantable cardiac devices, comprising a pulse generator, multiple sensing electrodes, a microprocessor-based control unit, a wireless communication module, and memory for dynamically adjusting pacing parameters based on real-time physiological data.  The system of claim 1, wherein the adaptive pacing algorithms include rate-responsive pacing based on physical activity.  The system of claim 1, further comprising an external monitoring system for remote data access and modification of pacing parameters.",
        "Sachin's SSN is 222-85-4836. His passport ID is 5484880UA.  Sachin's driver's license number is S9998888.  Sachin's bank account number is 70048841700216300.  His American express credit card number is 371449635398431.  His UK IBAN Code is AZ96AZEJ00000000001234567890.  ITIN number 993-77 0690.",
    ]

    if metadata:
        _metadata = {"authorized_identities": ["joe.smith@acme.org"]}
    else:
        _metadata = None

    if metadatas:
        # Metadata(source: fake news web url) for each text
        _metadata_list = [
            {"source": f"https://www.acme.org/news/{i}"}
            for i in range(1, len(texts) + 1)
        ]
    else:
        _metadata_list = None

    if ids:
        # Unique ids for each text (sha256 hash of text)
        _ids = [sha256(text.encode()).hexdigest() for text in texts]
    else:
        _ids = None
    return texts, _metadata, _metadata_list, _ids
